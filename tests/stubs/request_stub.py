from typing import Optional


class RequestStub:
    """
    Stub request to imitate a Discord request.

    This should only be used for testing.
    """

    def __init__(self, type: int, data: Optional[dict] = None):
        self.headers = {"X-Signature-Timestamp": "", "X-Signature-Ed25519": ""}
        self.data = data or {}

        self.type = type

    async def json(self) -> dict:
        """Get the json body of the request stub."""
        return {
            "type": self.type,
            "data": self.data
        }

    async def text(self) -> str:
        """Get the text body of the request stub."""
        return str(await self.json())
