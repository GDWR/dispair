import asyncio
import logging
from abc import ABC
from asyncio import AbstractEventLoop
from collections import ChainMap, defaultdict
from dataclasses import dataclass, field
from typing import Optional, Union

from aiohttp import ClientResponseError

from dispair.http.http_session import HttpSession, ApiPath
from dispair.models.interaction import Interaction
from dispair.models.response import Response
from dispair.utils.embed import Embed
from .missing_handler import MissingHandler
from .models import Handler, Option
from .router import Router

MISSING_HANDLER = MissingHandler()


@dataclass
class Command:
    """A registered command gathered from the DiscordAPI."""

    id: int
    application_id: int
    name: str
    description: str
    version: int
    default_permission: bool
    guild_id: Optional[int] = None
    options: Optional[list[Option]] = field(default_factory=list)

    @property
    def is_global(self) -> bool:
        """Return if the command is registered globally."""
        return self.guild_id is None

    def __hash__(self) -> int:
        return hash(self.name)


class Client(ABC):
    """Dispair Client."""

    def __init__(
            self,
            bot_token: str,
            app_id: str, *,
            missing_handler: MissingHandler = MISSING_HANDLER,
            log_level: int = 20,
            loop: AbstractEventLoop = None
    ):
        assert app_id is not None, "Missing App ID"
        assert bot_token is not None, "Missing Bot Token"
        self.bot_token = bot_token
        self.app_id = app_id
        self.missing_handler = missing_handler

        self._global_commands: dict[str, Command] = {}
        self._guild_commands: dict[int, dict[str, Command]] = defaultdict(dict)
        self._global_handlers: dict[str, Handler] = {}
        self._guild_handlers: dict[int, dict[str, Handler]] = defaultdict(dict)

        # Because we cannot query what guilds have put the bot into their server for just SlashCommands.
        # The best alternative is to keep a set of guilds we received interactions for, assign handler for etc.
        # This means we can keep them synced.
        self._known_guilds: set[int] = set()

        self._routers = []
        self._loop = loop or asyncio.get_event_loop()
        self._http_session = HttpSession(bot_token)
        self._logger = logging.getLogger("Client")
        self._logger.setLevel(log_level)

    @property
    def handlers(self) -> ChainMap[Union[str, int], Union[Handler, dict[str, Handler]]]:
        """Get the mapping for all handler."""
        return ChainMap(self._global_handlers, self._guild_handlers)

    @property
    def commands(self) -> ChainMap[Union[str, int], Union[Command, dict[str, Command]]]:
        """Get the mapping of all commands."""
        return ChainMap(self._global_commands, self._guild_commands)

    async def handle(self, interaction: Interaction) -> Response:
        """Handle an interaction."""
        if interaction.guild_id not in self._known_guilds:
            await self._sync_guild_commands(interaction.guild_id)
            self._known_guilds.add(interaction.guild_id)

        if guild_handlers := self.handlers.get(interaction.guild_id):
            handler = guild_handlers.get(interaction.name)
        else:
            handler = self.handlers.get(interaction.name)

        if handler is None:
            handler = self.missing_handler

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
        self._routers.append(router)
        for name, handler in router.handlers.items():
            if handler.is_global:
                self._global_handlers[name] = handler
            for guild in handler.guilds:
                if guild not in self._known_guilds:
                    self._known_guilds.add(guild)

                self._guild_handlers[guild][name] = handler

    async def _ensure_handler_registered(self, handler: Handler) -> None:
        if handler.is_global:
            if handler in self.commands:
                print("Assinged")
            else:
                print("Unassigned")
        else:
            for guild in handler.guilds:
                if self.commands[guild].get(handler.name) is None:
                    await self._register_handler(handler, guild)
                else:
                    self._logger.debug(f"Handler {handler.name} was already assigned")

    async def _sync_global_commands(self) -> None:
        self._logger.debug("Removing global commands that do not have assigned handlers")
        for handler in self.commands.values():
            if isinstance(handler, Command):
                if handler.is_global and handler.name not in self._global_handlers.keys():
                    await self._unregister_command(handler)

    async def _sync_guild_commands(self, guild: int) -> None:
        self._logger.debug(f"Syncing guild commands for guild: {guild}")
        guild_commands = await self._fetch_guild_commands(guild)

        for command in guild_commands.values():
            if command.name not in self.handlers[guild]:
                self._logger.debug(f"Unregistering unhandled command: {command.name}")
                await self._unregister_command(command, guild)

    async def _sync_all_guild_commands(self) -> None:
        for guild in self._known_guilds:
            await self._sync_guild_commands(guild)

    async def _register_handler(self, handler: Handler, guild: Optional[int] = None) -> None:
        """
        Register a handler with the client for incoming message to be handled by.

        If guild is None, it will be assigned globally.
        """
        self._logger.debug(f"Registering handler for: {handler.name} | {guild or 'Global'}")

        if guild is not None:
            await self._http_session.request(
                "POST",
                ApiPath("applications/{app_id}/guilds/{guild_id}/commands", app_id=self.app_id, guild_id=guild),
                json=handler.json
            )
        else:
            await self._http_session.request(
                "POST",
                ApiPath("applications/{app_id}/commands", app_id=self.app_id),
                json=handler.json
            )

    async def _unregister_command(self, command: Command, guild: Optional[int] = None) -> None:
        """
        Unregister a command.

        If guild is None, it will be removed globally.
        """
        self._logger.debug(f"Unregistering command for: {command.name} | {guild or 'Global'}")

        if guild is not None:
            await self._http_session.request(
                "DELETE",
                ApiPath(
                    "applications/{app_id}/guilds/{guild_id}/commands/{command_id}",
                    app_id=self.app_id,
                    guild_id=guild,
                    command_id=command.id
                ),
            )
        else:
            await self._http_session.request(
                "DELETE",
                ApiPath("applications/{app_id}/commands/{command_id}", app_id=self.app_id, command_id=command.id),
            )

    async def _fetch_all_global_commands(self) -> dict[str, Command]:
        """Request all global commands from the Discord API."""
        resp = await self._http_session.request(
            "GET",
            ApiPath("/applications/{app_id}/commands", app_id=self.app_id),
        )
        for command in [Command(**data) for data in resp]:
            self._global_commands[command.name] = command

        return self._global_commands

    async def _fetch_guild_commands(self, guild: int) -> dict[str, Command]:
        resp = await self._http_session.request(
            "GET",
            ApiPath("/applications/{app_id}/guilds/{guild_id}/commands", app_id=self.app_id, guild_id=guild),
        )
        for command in [Command(**data) for data in resp]:
            self._guild_commands[guild][command.name] = command
        return self._guild_commands[guild]

    async def _fetch_all_guild_commands(self) -> dict[int, dict[str, Command]]:
        """Request all known guild commands from the Discord API."""
        for guild in self._known_guilds:
            await self._fetch_guild_commands(guild)

        return self._guild_commands

    def run(self) -> None:
        """
        Begin running the bot.

        This base class will register all attached routers/handlers with the DiscordAPI.
        It will then Remove any unregistered handlers. This will block until the client is stopped.
        """
        loop = asyncio.get_event_loop()

        # Startup requests
        loop.run_until_complete(self._fetch_all_global_commands())
        loop.run_until_complete(self._fetch_all_guild_commands())

        for router in self._routers:
            for handler in router.handlers.values():
                self._logger.debug(f"Ensuring that {handler.name} command is assigned.")
                try:
                    loop.run_until_complete(self._ensure_handler_registered(handler))
                except ClientResponseError as err:
                    self._logger.error(f"Received HTTPError {err.status} while trying to assign handlers. Exiting...")
                    loop.run_until_complete(self.shutdown())
                    exit(-1)

        loop.run_until_complete(self._sync_global_commands())
        loop.run_until_complete(self._sync_all_guild_commands())

    async def shutdown(self) -> None:
        """Shutdown the bot, closing any resources being currently used."""
        self._logger.info("Client shutting down.")
        await self._http_session.kill()
