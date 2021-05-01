import asyncio
from abc import abstractmethod, ABC
from json import dumps

from aiohttp import web, ClientSession, ClientOSError
from aiohttp.web_request import Request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


class Response:
    def __init__(self, content: str):
        self.content = content

    def json(self) -> str:
        return dumps({
            "type": 4,
            "data": {
                "tts": False,
                "content": self.content,
                "embeds": [],
                "allowed_mentions": {"parse": []}
            }
        })


class InteractionData:
    id: int
    name: str
    resolved: dict
    options: dict


class Interaction:

    def __init__(self, _id, application_id, _type, data, guild_id, channel_id, member, user, token):
        self.id = _id
        self.application_id = application_id
        self.type = _type
        self.data = data
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.member = member
        self.user = user
        self.token = token

    @property
    def name(self) -> str:
        return self.data.get("name")


class Handler(ABC):
    name: str
    description: str

    @abstractmethod
    async def handle(self, interaction: Interaction) -> Response:
        raise NotImplementedError()


class Router:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def __call__(self, *args, **kwargs):
        return self.interaction(*args, **kwargs)

    def interaction(self, name: str, description: str):
        name = name.lower()

        class Handle(Handler):
            def __init__(self):
                self.name = name
                self.description = description

            async def handle(self, interaction):
                return await self.function(interaction)

            def __call__(self, func, *args, **kwargs):
                self.function = func

        handler = Handle()
        self.handlers[name] = handler
        return handler


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
                await session.post(
                    f"https://discord.com/api/v8/applications/{self.application_id}/guilds/566407576686952480/commands",
                    data=dumps({"name": handler.name, "description": handler.description, "options": []}),
                    headers={"Authorization": f"Bot {self.bot_token}", "Content-Type": "application/json"}
                )
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
        return response
