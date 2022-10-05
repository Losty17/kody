from discord import Interaction
from discord.app_commands import command, locale_str
from kody import KodyBot
from kody.dashboard import DashboardEmbed, DashboardView
from kody.db.repositories import UserRepository
from kody.modules import BaseCog


class Dashboard(BaseCog):
    def __init__(self, bot: KodyBot) -> None:
        super().__init__(bot)

    @command(
        name=locale_str("dashboard", namespace="commands"),
        description=locale_str("dashboarddesc", namespace="commands")
    )
    async def dashboard(self, i: Interaction):
        user_repo = UserRepository()
        user = user_repo.get(i.user.id)

        embed = DashboardEmbed(i.user, user)
        view = DashboardView(user)

        await i.response.send_message(embed=embed, view=view)


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Dashboard(bot))
