from .member import Member


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

    @property
    def author(self) -> Member:
        return Member(**self.member)