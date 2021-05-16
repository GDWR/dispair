from json import dumps
from typing import Optional

from .embed import Embed


class Response:
    """
    Response to be sent back to Discord.

    This contains the text content, embeds and mention permissions.
    """

    def __init__(self, content: str = "", *, embed: Optional[Embed] = None):
        self.content = content
        self.embeds = []
        if embed:
            self.embeds.append(embed)

    def json(self) -> dict:
        """Return the json representation of the Response."""
        return {
            "type": 4,
            "data": {
                "tts": False,
                "content": self.content,
                "embeds": [embed.json() for embed in self.embeds],
                "allowed_mentions": {"parse": []}
            }
        }
