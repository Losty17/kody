from os import getenv
from discord import Intents

APP_ID = int(getenv("APP_ID") or 0)
OWNER_ID = int(getenv("OWNER_ID") or 0)
BOT_TOKEN = getenv("BOT_TOKEN") or ""
BOT_PREFIX = getenv("BOT_PREFIX") or ";"
BOT_INTENTS = Intents.all()
