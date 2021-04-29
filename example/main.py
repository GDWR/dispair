from os import environ
from dispair import Client
from handlers.fun import router

client = Client(
    environ.get("BOT_TOKEN"),
    environ.get("APP_ID"),
    environ.get("APP_PUBLIC_KEY")
)

client.attach_router(router)

client.run()
