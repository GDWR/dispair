import inspect
from abc import ABC, abstractmethod

from .option import Option
from .response import Response
from .member import Member
from .interaction import Interaction


class Handler(ABC):
    name: str
    description: str
    options: list[Option]

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.options = []

    def __call__(self, func, *args, **kwargs):
        self.function = func
        self._create_options()

    def _create_options(self):
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
        raise NotImplementedError()

    @property
    def json(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "options": [option.json for option in self.options],
        }
