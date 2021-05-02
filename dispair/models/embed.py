from datetime import datetime


class Embed:
    title: str
    description: str
    url: str
    timestamp: datetime
    color: int
    footer: dict
    image: dict
    thumbnail: dict
    video: dict
    provider: dict
    author: dict
    fields: list[dict]

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def json(self) -> dict:
        return {
            "title": self.title,
            "type": "rich",
            "description": self.description,

        }