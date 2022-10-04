from discord.ext.commands import Cog

from kody.kodybot import KodyBot

class BaseCog(Cog):
    def __init__(self, bot: KodyBot) -> None:
        self.bot = bot
