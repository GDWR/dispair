from __future__ import annotations


class Member:
    """
    Discord Guild Member.

    https://discord.com/developers/docs/resources/guild#guild-member-object
    """

    id: int
    username: str
    discriminator: str
    avatar: str

    def __init__(self, **kwargs):
        print(kwargs)

    @classmethod
    async def from_userid(cls, guild_id: int, user_id: int) -> Member:
        """Fetch a Guild Member from ID."""
        member = cls()
        member.id = user_id
        member.guild = guild_id
        return member
