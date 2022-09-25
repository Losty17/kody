import os

from discord.ext import commands

from ...kody import KodyBot
from .database import db
from .groups import KodyStaff


class Staff(commands.Cog):
    kody = KodyStaff()

    def __init__(self, bot: KodyBot) -> None:
        self.bot = bot

        # --- Debug ---
        if os.getenv("ENVIRONMENT").lower() != "production":
            db.sync()


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Staff(bot))
