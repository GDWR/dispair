"""
HTTPSession has been heavily influnced by the works of vcokltfre.

https://github.com/vcokltfre/Corded/blob/master/corded/http
"""

import asyncio
import logging
from asyncio import Lock, AbstractEventLoop
from typing import Optional, Literal

from aiohttp import ClientSession, ClientWebSocketResponse

from ..constants import API_VERSION


class RateLimiter:
    """Discord RateLimiter that uses buckets based on the requested data."""

    def __init__(self):
        self._locks: dict[str, Lock] = {}

    def __getitem__(self, item: str) -> Lock:
        """Get the appropriate lock or create a new one."""
        if lock := self._locks.get(item):
            return lock
        self._locks[item] = Lock()
        return self._locks[item]


class ApiPath:
    """Represent the APIPath, used to generate Bucket strings."""

    def __init__(self, path: str, **params: dict):
        self.path = path

    @property
    def url(self) -> str:
        """Get the absolute url for the api route."""
        return HttpSession.api_base + self.path

    @property
    def bucket(self) -> str:
        """Get the bucket string to use for rate limiting."""
        return "Need to do"  # TODO: This.


class HttpSession:
    """HTTPSession containing a aiohttp.ClientSession with Rate Limits."""

    api_base = f"https://discord.com/api/v{API_VERSION}"

    def __init__(self, bot_token: Optional[str] = None, *, loop: AbstractEventLoop = None):
        self.rate_limiter = RateLimiter()
        self.loop = loop or asyncio.get_event_loop()
        self._logger = logging.getLogger("http_session")

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
            method: Literal["GET", "POST"],
            path: ApiPath,
            **kwargs
    ) -> Optional[dict]:
        """
        Make a request using the aiohttp.ClientSession.

        If the request hits the Discord Rate Limit, the
        request will wait until the Rate Limit has been
        passed.
        """
        async with self.rate_limiter[path.bucket]:
            resp = await self._session.request(method, path.url, **kwargs)
            if resp.content_type == "application/json":
                return await resp.json()

    async def ws_connect(self, url: str, **kwargs) -> ClientWebSocketResponse:
        """Expose the `ws_connect` method of the session cleanly."""
        return await self._session.ws_connect(url, **kwargs)

    async def kill(self) -> None:
        """Close the HttpSession."""
        await self._session.close()
