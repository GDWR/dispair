from .models import Handler, Interaction, Member, Response


class Router:
    """Router for creating Interaction Handlers."""

    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def __call__(self, *args, **kwargs) -> Handler:
        """Decorator to create a interaction handler."""
        return self.interaction(*args, **kwargs)

    def interaction(self, name: str, description: str) -> Handler:
        """Create a Interaction Handler."""
        name = name.lower()

        class Handle(Handler):
            async def handle(self, interaction: Interaction) -> Response:
                """Overwrite the handle method with handler's function object."""
                options = {}

                if data_options := interaction.data.get("options"):
                    for option in data_options:
                        if option["type"] == 3:
                            options[option["name"]] = str(option["value"])
                        elif option["type"] == 4:
                            options[option["name"]] = int(option["value"])
                        elif option["type"] == 5:
                            options[option["name"]] = bool(option["value"])
                        elif option["type"] == 6:
                            options[option["name"]] = await Member.from_userid(option["value"])

                return await self.function(interaction, **options)

        handler = Handle(name, description)
        self.handlers[name] = handler
        return handler
