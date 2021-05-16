import asyncio
from asyncio import Queue

from dispair.client import Client
from dispair.models import Interaction


class ClientStub(Client):
    def __init__(self):
        super().__init__("", "")
        self.msg_in = Queue()
        self.msg_out = Queue()

    def run(self) -> None:
        async def _main_loop():
            while True:
                try:
                    msg = await self.msg_in.get()
                    if not isinstance(msg, Interaction):
                        raise TypeError("Received a message that wasn't an interaction.")
                    resp = await self.handle(msg)
                    await self.msg_out.put(resp)
                except Exception as e:
                    break

        self.task = asyncio.create_task(_main_loop())

    async def kill(self):
        await self._http_session.kill()
        self.task.cancel()

    async def _register_handler(self, *args, **kwargs):
        ...
