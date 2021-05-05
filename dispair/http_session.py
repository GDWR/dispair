import asyncio

from aiohttp import ClientResponseError, ClientSession


class HttpSession:
    """HTTPSession containing a aiohttp.ClientSession with Rate Limits."""

    def __init__(self, bot_token: str):
        self.rate_lock = asyncio.Lock()
        self._session = ClientSession(
            headers={
                "Authorization": f"Bot {bot_token}",
                "Content-Type": "application/json"
            }
        )

    async def request(self, url: str, json: str) -> dict:
        """
        Make a request using the aiohttp.ClientSession.

        If the request hits the Discord Rate Limit, the
        request will wait until the Rate Limit has been
        passed.
        """
        async with self.rate_lock:
            response = await self._session.post(url, data=json)
            try:
                response.raise_for_status()
                return await response.json()
            except ClientResponseError as err:
                if err.status == 429:
                    remaining = float(response.headers.get("X-RateLimit-Reset"))
                    await asyncio.sleep(remaining)
                    return await self.request(url, json)
                else:
                    raise err

    async def kill(self) -> None:
        """Close the HttpSession."""
        await self._session.close()
