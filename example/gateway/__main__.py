import os

import logging

from dispair import GatewayClient as Client
from dotenv import load_dotenv

from example.handlers.fun import router

def main() -> None:
    if os.getenv("ENVIRONMENT") is None:
        load_dotenv(dotenv_path='.env')

    client = Client(
        os.getenv("BOT_TOKEN"),
        os.getenv("APP_ID"),
        log_level=logging.DEBUG
    )

    client.attach_router(router)

    client.run()


if __name__ == "__main__":
    main()
