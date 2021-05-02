from __future__ import annotations

import asyncio

from json import dumps

from aiohttp import web, ClientSession, ClientOSError
from aiohttp.web_request import Request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from .router import Router
from .models import Handler, Response, Embed, Interaction


class Client:
    def __init__(self, bot_token: str, application_id: str, application_public_key: str,
                 interaction_endpoint: str = "/interactions", port: int = 80):
        self._app = web.Application()
        self._http_session = ClientSession()
        self._routers: list[Router] = []
        self.interaction_endpoint = interaction_endpoint
        assert self.interaction_endpoint[0] == "/", "Interaction Endpoint must begin with /"
        self.port = port
        self._verify_key = VerifyKey(bytes.fromhex(application_public_key))
        self.application_id = application_id
        self.bot_token = bot_token

    def attach_router(self, router: Router):

        for handler in router.handlers.values():
            asyncio.ensure_future(self._register_handler(handler))

        self._routers.append(router)

    def run(self) -> None:
        self._app.add_routes((web.post(self.interaction_endpoint, self._interaction),))
        web.run_app(self._app, port=self.port)

    async def _interaction(self, request: Request):

        if not (timestamp := request.headers.get("X-Signature-Timestamp")) \
                or not (ed25519 := request.headers.get("X-Signature-Ed25519")):
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

    async def _register_handler(self, handler: Handler):
        async with self._http_session as session:
            try:
                resp = await session.post(
                    f"https://discord.com/api/v8/applications/{self.application_id}/guilds/566407576686952480/commands",
                    data=dumps(handler.json),
                    headers={"Authorization": f"Bot {self.bot_token}", "Content-Type": "application/json"}
                )
                if resp.status != 200:
                    print(await resp.json())

            except ClientOSError as e:
                print(e)

    async def _handle(self, payload) -> Response:
        interaction = Interaction(
            _id=payload["id"],
            application_id=payload["application_id"],
            _type=payload["type"],
            data=payload["data"],
            guild_id=payload["guild_id"],
            channel_id=payload["channel_id"],
            member=payload["member"],
            user=payload.get("user"),
            token=payload["token"],
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
