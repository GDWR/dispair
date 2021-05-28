"""
HTTPSession has been heavily influenced by the works of vcokltfre.

https://github.com/vcokltfre/Corded/blob/master/corded/http
"""

import asyncio
import logging
import math
import time
from asyncio import Lock, AbstractEventLoop
from typing import Optional, Literal, Union

from aiohttp import ClientSession, ClientWebSocketResponse, ClientResponseError

from ..constants import API_VERSION


class LockContext:
    """Context manager for RateLimiting lock, Allows for releasing after `n` time."""

    def __init__(self, lock: Lock):
        self._logger = logging.getLogger("Lock")
        self._logger.setLevel(logging.DEBUG)
        self._lock = lock
        self._acquired = False

    async def __aenter__(self):
        await self._lock.acquire()
        self._acquired = True
        return self

    async def __aexit__(self, *argsb):
        if self._acquired:
            self._lock.release()
            self._acquired = False

    def __exit__(self, *args):
        if self._acquired:
            self._lock.release()
            self._acquired = False

    async def release_at(self, unix_time: Union[int, float]) -> None:
        """Release the lock at a specific time."""
        seconds = math.ceil(unix_time - time.time())
        self._logger.debug(f"Releasing lock in {seconds} seconds")
        await asyncio.sleep(seconds)
        self._lock.release()
        self._acquired = False


class RateLimiter:
    """Discord RateLimiter that uses buckets based on the requested data."""

    def __init__(self):
        self._logger = logging.getLogger("RateLimiter")
        self._logger.setLevel(logging.DEBUG)
        self._locks: dict[str, Lock] = {}

    def __getitem__(self, item: str) -> LockContext:
        """Get the appropriate lock or create a new one."""
        return self.get(item)

    def get(self, item: str) -> LockContext:
        """Get the appropriate lock or create a new one."""
        if lock := self._locks.get(item):
            self._logger.debug(f"<{item}> Acquired lock")
            return LockContext(lock)

        self._logger.debug(f"<{item}> Generating new lock")
        self._locks[item] = Lock()
        return LockContext(self._locks[item])


class ApiPath:
    """Represent the APIPath, used to generate Bucket strings."""

    def __init__(self, path: str, **params):
        self.path = path.format(**params)
        self._raw_path = path
        self.params = params

    @property
    def url(self) -> str:
        """Get the absolute url for the api route."""
        return HttpSession.api_base + self.path

    @property
    def bucket(self) -> str:
        """Get the bucket string to use for rate limiting."""
        guild_id = self.params.get("guild_id", 0)
        channel_id = self.params.get("channel_id", 0)
        webhook_id = self.params.get("webhook_id", 0)
        interaction_id = self.params.get("interaction_id", 0)
        interaction_token = self.params.get("interaction_token", 0)

        return f"{guild_id}-{channel_id}-{webhook_id}-{interaction_id}-{interaction_token}::{self._raw_path}"


class HttpSession:
    """HTTPSession containing a aiohttp.ClientSession with Rate Limits."""

    api_base = f"https://discord.com/api/v{API_VERSION}/"

    def __init__(self, bot_token: Optional[str] = None, *, loop: AbstractEventLoop = None):
        self.rate_limiter = RateLimiter()
        self.loop = loop or asyncio.get_event_loop()
        self._logger = logging.getLogger("http_session")
        self._logger.setLevel(logging.DEBUG)

        if bot_token:
            self._session = ClientSession(
                headers={
                    "Authorization": f"Bot {bot_token}",
                    "Content-Type": "application/json"
                },
                loop=self.loop
            )
        else:
            self._session = ClientSession(loop=self.loop)

    async def request(
            self,
            method: Literal["GET", "POST", "DELETE"],
            path: ApiPath,
            **kwargs
    ) -> Optional[dict]:
        """
        Make a request using the aiohttp.ClientSession.

        If the request hits the Discord Rate Limit, the
        request will wait until the Rate Limit has been
        passed.
        """
        async with self.rate_limiter[path.bucket] as lock:
            resp = await self._session.request(method, path.url, **kwargs)

            if resp.content_type == "application/json":
                content = await resp.json()
            else:
                self._logger.debug(f"Received response content_type: {resp.content_type}")
                return
            try:
                resp.raise_for_status()
            except ClientResponseError as err:
                self._logger.error(str(err))
                raise err

            remaining = resp.headers.get("x-ratelimit-remaining", "1")

            if int(remaining) == 0:
                reset = resp.headers["x-ratelimit-reset"]
                await lock.release_at(float(reset))

        return content

    async def ws_connect(self, url: str, **kwargs) -> ClientWebSocketResponse:
        """Expose the `ws_connect` method of the session cleanly."""
        return await self._session.ws_connect(url, **kwargs)

    async def kill(self) -> None:
        """Close the HttpSession."""
        await self._session.close()
