import asyncio
import logging
import platform

from aiohttp import WSMsgType

from dispair.models import Interaction
from dispair.http import ApiPath
from dispair.client import Client
from dispair.exceptions import HandlerNotDefined
from dispair.constants import API_VERSION


class GatewayClient(Client):
    url: str
    shards: int
    session_start_limit: dict

    async def _perform_handshake(self) -> None:
        self._logger.debug("Awaiting first message")
        msg = await self._ws_session.receive()
        self._logger.debug("Received first message")
        payload = msg.json()
        assert payload["op"] == 10, "Gateway did not respond with handshake"
        self.heartbeat_interval_ms = payload["d"]["heartbeat_interval"]
        self._logger.debug("Waiting heartbeat interval")
        # await asyncio.sleep((self.heartbeat_interval_ms * random.random()) / 1_000)

    async def _identify(self) -> None:
        self._logger.debug("Identifying through Gateway")
        await self._ws_session.send_json({
            "op": 2,
            "d": {
                "token": self.bot_token,
                "intents": 513,
                "properties": {
                    "$os": platform.system(),
                    "$browser": "Dispair",
                    "$device": "Dispair"
                }
            }
        })

    async def handle_loop(self) -> None:
        await self._perform_handshake()
        await self._identify()

        self._logger.debug("Beginning main handle loop")
        while self._loop.is_running():
            try:
                msg = await self._ws_session.receive(timeout=self.heartbeat_interval_ms / 1_000)
                if msg.type == WSMsgType.TEXT:
                    payload = msg.json()
                    if payload["t"] == "INTERACTION_CREATE":
                        data = payload["d"]
                        interaction = Interaction(
                            _id=data["id"],
                            application_id=data["application_id"],
                            _type=data["type"],
                            data=data["data"],
                            guild_id=data["guild_id"],
                            channel_id=data["channel_id"],
                            member=data["member"],
                            user=data["member"]["user"],
                            token=data["token"],
                        )
                        self._logger.debug(f"Received interaction: {interaction}")
                        try:
                            response = await self.handle(interaction)
                        except HandlerNotDefined:
                            self._logger.info(f"No handler defined for interaction: {interaction.name}")
                            continue
                        self._logger.debug(f"Handled with response: {response}")

                        await self._http_session.request(
                            "POST",
                            ApiPath(f"/interactions/{interaction.id}/{interaction.token}/callback"),
                            json=response.json()
                        )

                elif msg.type == WSMsgType.CLOSED:
                    break
            except asyncio.TimeoutError:
                self._logger.info("Sending heartbeat message")
                await self._ws_session.send_json({"op": 1})

        self._logger.error("Channel was closed")

    async def connect_to_gateway(self) -> None:
        self._logger.debug("Connecting to Gateway")
        self._ws_session = await self._http_session.ws_connect(self.url + f"/?v={API_VERSION}&encoding=json")
        self._logger.debug("Connected to Gateway")

    async def get_gateway(self) -> None:
        self._logger.debug("Requesting Gateway")
        req = await self._http_session.request("GET", ApiPath("/gateway/bot"))
        self._logger.debug("Received Gateway")
        self.url = req["url"]
        self.shards = req["shards"]
        self.session_start_limit = req["session_start_limit"]

    async def _startup(self) -> None:
        self._logger.debug("Starting up GatewayClient")
        await self.get_gateway()
        await self.connect_to_gateway()
        await self.handle_loop()
        await self._shutdown()

    async def _shutdown(self) -> None:
        await super().shutdown()

    def run(self) -> None:
        self._logger.log(logging.DEBUG, "Starting to run GatewayClient")

        asyncio.get_event_loop().run_until_complete(self._startup())
