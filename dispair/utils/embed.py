from datetime import datetime
from typing import Optional

from dispair.utils.colour import Colour


class Embed:
    """
    Discord Embed object.

    https://discord.com/developers/docs/resources/channel#embed-object
    """

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

    def __init__(self, title: str, description: Optional[str] = None, colour: Optional[Colour] = None):
        self.title = title
        self.description = '' if description is None else description
        self.color = Colour(0, 0, 0) if colour is None else colour

    def json(self) -> dict:
        """Json representation of the Embed."""
        return {
            "title": self.title,
            "type": "rich",
            "description": self.description,
            "color": self.color.decimal
        }
