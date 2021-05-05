from .member import Member


class Interaction:
    """
    Discord Interaction.

    https://discord.com/developers/docs/interactions/slash-commands#interaction
    """

    def __init__(
            self,
            _id: int,
            application_id: int,
            _type: int,
            data: dict,
            guild_id: int,
            channel_id: int,
            member: dict,
            user: dict,
            token: str
    ):
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
        """Get the name of the Interaction command."""
        return self.data.get("name")

    @property
    def author(self) -> Member:
        """Get the author of Interaction."""
        return Member(**self.member)
