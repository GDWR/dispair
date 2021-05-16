from json import dumps

from aiohttp import web
from aiohttp.web_request import Request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from .client import Client
from .models import Response, Interaction
from .router import Router
from .utils import Embed


class WebhookClient(Client):
    """Client for webhook usage."""

    def __init__(self, bot_token: str, application_id: str, application_public_key: str,
                 interaction_endpoint: str = "/interactions", port: int = 80):
        super().__init__(bot_token)
        self._app = web.Application()
        self._routers: list[Router] = []
        self._pub_key = application_public_key
        self.interaction_endpoint = interaction_endpoint
        assert self.interaction_endpoint[0] == "/", "Interaction Endpoint must begin with /"
        self.port = port
        self.application_id = application_id

    async def _interaction(self, request: Request) -> web.Response:
        """Aiohttp endpoint handler for DiscordInteractions."""
        if (timestamp := request.headers.get("X-Signature-Timestamp")) is None \
                or (ed25519 := request.headers.get("X-Signature-Ed25519")) is None:
            return web.Response(status=401, reason="Unauthorised")

        try:
            self._verify_key.verify((timestamp + await request.text()).encode(), bytes.fromhex(ed25519))
        except BadSignatureError:
            return web.Response(status=401, reason="Unauthorised")

        payload = await request.json()
        if payload.get('type') == 1:
            return web.Response(status=200, text=dumps({"type": 1}), content_type="application/json")
        else:
            response = await self._handle(payload)
            return web.Response(status=200, text=response.json(), content_type="application/json")

    async def _handle(self, payload: dict) -> Response:
        interaction = Interaction(
            _id=payload.get("id"),
            application_id=payload.get("application_id"),
            _type=payload.get("type"),
            data=payload.get("data"),
            guild_id=payload.get("guild_id"),
            channel_id=payload.get("channel_id"),
            member=payload.get("member"),
            user=payload.get("user"),
            token=payload.get("token"),
        )
        router = self._routers[0]
        handler = router.handlers.get(interaction.name)
        response = await handler.handle(interaction)
        if isinstance(response, Response):
            return response
        elif isinstance(response, (int, str)):
            return Response(content=str(response))
        elif isinstance(response, Embed):
            return Response(embed=response)
        else:
            try:
                return Response(content=str(response))
            except ValueError:
                raise ValueError(f"Cannot send type {response} as a Interaction response.")

    def run(self) -> None:
        """Start the Dispair client."""
        self._verify_key = VerifyKey(bytes.fromhex(self._pub_key))
        self._app.add_routes((web.post(self.interaction_endpoint, self._interaction),))
        web.run_app(self._app, port=self.port)
