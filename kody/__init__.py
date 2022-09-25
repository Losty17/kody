from os import getenv

from discord import Intents
from dotenv import load_dotenv

from .kody import KodyBot

load_dotenv()

kody = KodyBot(
    ">",
    intents=Intents.all(),
    application_id=int(getenv("APP_ID")),
    owner_id=int(getenv("OWNER_ID"))
)

kody.run(getenv("BOT_TOKEN"))
