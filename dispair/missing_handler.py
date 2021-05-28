from dispair.models import Interaction


class MissingHandler:
    """
    Response for a missing handler. This can be subclassed to add your own
    missing handler functionality.
    """

    async def handle(self, inter: Interaction, *args, **kwargs) -> str:
        return f"> Command {inter.name} is not supported"
