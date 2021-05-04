from datetime import datetime
from typing import Optional

from .colour import Colour


class Embed:
    title: str
    description: str
    url: str
    timestamp: datetime
    color: Colour
    footer: dict
    image: dict
    thumbnail: dict
    video: dict
    provider: dict
    author: dict
    fields: list[dict]

    def __init__(self, title: str, description: Optional[str] = None, colour: Colour = Colour(0, 0, 0)):
        self.title = title
        self.description = '' if description is None else description
        self.color = colour

    def json(self) -> dict:
        return {
            "title": self.title,
            "type": "rich",
            "description": self.description,
            "color": self.color.decimal
        }
