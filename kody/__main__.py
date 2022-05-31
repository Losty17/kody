from os import getenv

from discord import Intents
from dotenv import load_dotenv

from .kody import KodyBot
from . import bot

load_dotenv()


bot.run(getenv("BOT_TOKEN"))
