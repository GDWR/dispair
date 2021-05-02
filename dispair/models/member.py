from __future__ import annotations

class Member:
    id: int
    username: str
    discriminator: str
    avatar: str

    def __init__(self, **kwargs):
        print(kwargs)

    @classmethod
    async def from_userid(cls, user_id: int) -> Member:
        member = cls()
        member.id = user_id
        return member