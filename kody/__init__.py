import i18n
from os import listdir
from dotenv import load_dotenv
from kody.kodybot import KodyBot

load_dotenv()

from .constants import *

for folder in listdir("kody/i18n"):
    i18n.load_path.append(f"kody/i18n/{folder}")

i18n.set("fallback", "en")

kody = KodyBot(
    BOT_PREFIX,
    intents=BOT_INTENTS,
    application_id=APP_ID,
    owner_id=OWNER_ID
)

kody.run(BOT_TOKEN)
