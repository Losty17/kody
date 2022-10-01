from os import getenv, listdir

from discord import Intents
from dotenv import load_dotenv

import i18n

from .kody import KodyBot

load_dotenv()

for folder in listdir("kody/i18n"):
    i18n.load_path.append(f"kody/i18n/{folder}")

i18n.set("fallback", "en")

kody = KodyBot(
    ">",
    intents=Intents.all(),
    application_id=int(getenv("APP_ID")),
    owner_id=int(getenv("OWNER_ID"))
)

kody.run(getenv("BOT_TOKEN"))
