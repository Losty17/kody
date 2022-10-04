import os

from discord.ext import commands

from kody.db import Database
from kody.kodybot import KodyBot
from .groups import KodyStaff


class Staff(commands.Cog):
    kody = KodyStaff()

    def __init__(self, bot: KodyBot) -> None:
        self.bot = bot

        # --- Debug ---
        if os.getenv("ENVIRONMENT").lower() != "production":
            Database.sync()


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Staff(bot))
