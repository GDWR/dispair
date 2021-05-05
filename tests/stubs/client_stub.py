import asyncio
from asyncio import Queue

from dispair import Client
from tests.stubs.verifykey_stub import VerifyKeyStub


class ClientStub(Client):
    def __init__(self):
        super().__init__("", "", "")
        self.msg_in = Queue()
        self.msg_out = Queue()

    def run(self) -> None:
        self._verify_key = VerifyKeyStub()

        async def _main_loop():
            while True:
                try:
                    msg = await self.msg_in.get()
                    resp = await self._interaction(msg)
                    await self.msg_out.put(resp)
                except Exception as e:
                    break

        self.task = asyncio.create_task(_main_loop())

    async def kill(self):
        await self._http_session.kill()
        self.task.cancel()

    async def _register_handler(self, *args, **kwargs):
        ...
