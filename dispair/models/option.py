class Option:
    """
    Discord Interaction option.

    https://discord.com/developers/docs/interactions/slash-commands#applicationcommandoption
    """

    name: str
    description: str
    type: int
    required: bool

    def __init__(
            self,
            *,
            name: str = None,
            desc: str = "",
            required: bool = True
    ):
        self.description = desc
        self.name = name
        self.required = required

    def __repr__(self) -> str:
        return f"<{self.__class__} object: {self.name}>"

    @property
    def json(self) -> dict:
        """Return the json representation of the Option."""
        assert self.name is not None, "an Option was not assigned a Name"

        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "required": self.required,
        }
