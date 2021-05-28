import inspect
from abc import ABC, abstractmethod
from typing import Callable

from .interaction import Interaction
from .member import Member
from .option import Option
from .response import Response


class Handler(ABC):
    """
    Base class of the Interaction Handlers.

    The functionality for the majority of the handler
    is defined here. Due to the need to overwrite the
    handler function using decorators, this is abstract.
    """

    name: str
    description: str
    _global: bool
    options: list[Option]
    guilds: list[int]

    def __init__(self, name: str, description: str, _global: bool, guilds: list[int]):
        self.name = name
        self.description = description
        self.options = []
        self._global = _global
        self.guilds = guilds

    def __call__(self, func: Callable, *args, **kwargs) -> None:  # noQA: D102
        self.function = func
        self._create_options()

    def _create_options(self) -> None:
        params = inspect.signature(self.function).parameters

        for _, hint in params.items():
            if hint.annotation == Interaction:
                continue

            if isinstance(hint.default, Option):
                option = hint.default
                if option.name is None:
                    option.name = str(hint.name)
                if option.description is None:
                    option.description = " "
            else:
                option = Option(name=hint.name, desc=" ")

            if hint.annotation is str:
                option.type = 3
            elif hint.annotation is int:
                option.type = 4
            elif hint.annotation is bool:
                option.type = 5
            elif hint.annotation is Member:
                option.type = 6
            else:
                raise ValueError(f"Cannot convert parameter of type: {hint.annotation}")

            self.options.append(option)

    @abstractmethod
    async def handle(self, interaction: Interaction) -> Response:
        """Replaced with the Interaction Handler when added to a router."""
        raise NotImplementedError()

    @property
    def is_global(self) -> bool:
        return self._global

    @property
    def json(self) -> dict:
        """Return the json form off the Interaction Handler."""
        return {
            "name": self.name,
            "description": self.description,
            "options": [option.json for option in self.options],
        }
