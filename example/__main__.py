import os

from dispair import Client
from dotenv import load_dotenv

from handlers.fun import router


def main() -> None:
    if os.getenv("ENVIRONMENT") is None:
        load_dotenv(dotenv_path='.env')

    client = Client(
        os.getenv("BOT_TOKEN"),
        os.getenv("APP_ID"),
        os.getenv("APP_PUBLIC_KEY"),
    )

    client.attach_router(router)

    client.run()


if __name__ == "__main__":
    main()
