from typing import Optional


class RequestStub:
    def __init__(self, type: int, data: Optional[dict] = None):
        self.headers = {"X-Signature-Timestamp": "", "X-Signature-Ed25519": ""}
        self.data = data or {}

        self.type = type

    async def json(self):
        return {
            "type": self.type,
            "data": self.data
        }

    async def text(self):
        return str(await self.json())
