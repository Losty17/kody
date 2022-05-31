from .kody import KodyBot, Kody


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Kody(bot))
