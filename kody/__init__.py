from os import getenv

from discord import Intents
from dotenv import load_dotenv

from .kody import KodyBot

load_dotenv()

intents = Intents.all()

bot = KodyBot("k!", intents=intents, application_id=getenv(
    "APP_ID"), owner_id=getenv("OWNER_ID"))
