# Getting started

## Installation
_Prerequisite: [Install Python 3.8+](https://www.python.org/) on your local environment._

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dispair.

```cmd
pip install dispair
```

## QuickStart

```python
from dispair import Router
from dispair import WebhookClient

router = Router()

@router.interaction(name="8ball", description="Let the 8ball take the wheel")
async def _8ball(inter: Interaction):
    answer = random.choice(["Yes", "No", "Maybe"])
    return f"> {answer}"

def main() -> None:
    if os.getenv("ENVIRONMENT") is None:
        load_dotenv(dotenv_path='.env')

    client = WebhookClient(
        os.getenv("BOT_TOKEN"),
        os.getenv("APP_ID"),
        os.getenv("APP_PUBLIC_KEY"),
    )

    client.attach_router(router)

    client.run()


if __name__ == "__main__":
    main()
```
In this quickstart example, we:
- Create a `dispair.Router` and create an interaction route
- Define a `dispair.WebhookClient` and pass in our necessary environment variables: our discord `BOT_TOKEN`,
our discord `APP_ID`, and our discord `APP_PUBLIC_KEY`, all of which we can find at the
[Discord Developer Portal](https://discord.com/developers/applications)
- Run our client
