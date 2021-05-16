import asyncio
import logging
from abc import ABC
from asyncio import AbstractEventLoop
from json import dumps

from .router import Router
from dispair.models.interaction import Interaction
from dispair.models.response import Response
from dispair.models.embed import Embed
from dispair.http.http_session import HttpSession, ApiPath
from dispair.exceptions import HandlerNotDefined


class Client(ABC):
    """Dispair Client."""

    def __init__(self, bot_token: str, app_id: str, *, log_level: int = 20, loop: AbstractEventLoop = None):
        self.bot_token = bot_token
        self.app_id = app_id

        self._routers = []
        self._loop = loop or asyncio.get_event_loop()
        self._http_session = HttpSession(bot_token)
        self._logger = logging.getLogger("Client")
        self._logger.setLevel(log_level)

    async def handle(self, interaction: Interaction) -> Response:
        router = self._routers[0]
        handler = router.handlers.get(interaction.name)
        if handler is None:
            raise HandlerNotDefined()

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

    def attach_router(self, router: Router) -> None:
        """Attach a router to the Client."""
        for handler in router.handlers.values():
            asyncio.ensure_future(self._register_handler(handler))

        self._routers.append(router)

    async def _register_handler(self, handler) -> None:
        await self._http_session.request(
            "POST",
            ApiPath(f"applications/{self.app_id}/guilds/566407576686952480/commands"),  # TODO: Dynamic guild ids
            json=dumps(handler.json)
        )

    def run(self) -> None:
        raise NotImplementedError()

    async def shutdown(self) -> None:
        self._logger.info("Client shutting down.")
        await self._http_session.kill()
