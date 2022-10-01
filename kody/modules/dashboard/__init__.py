import i18n
from discord import Interaction
from discord.app_commands import Choice, choices, command, describe, locale_str
from kody import KodyBot
from kody.db.repositories import UserRepository
from kody.modules import BaseCog
from kody.modules.dashboard.home import DashboardEmbed, DashboardView


class Dashboard(BaseCog):
    def __init__(self, bot: KodyBot) -> None:
        super().__init__(bot)

    @command(name=locale_str("commands_language"))
    @choices(language=[
        Choice(name="Português", value="pt"),
        Choice(name="English", value="en")
    ])
    @describe(language="Idioma desejado")
    async def language(self, interaction: Interaction, language: str):
        """ Mude o idioma do bot """
        user_repo = UserRepository()
        user = user_repo.get(interaction.user.id)

        user.locale = language
        user_repo.update(user)

        i18n.set("locale", language)

        await interaction.response.send_message(
            f'Language set to: {language}', ephemeral=True
        )

    @command(
        name=locale_str("dashboard", namespace="commands"),
        description=locale_str("dashboarddesc", namespace="commands")
    )
    async def dashboard(self, interaction: Interaction):
        user_repo = UserRepository()
        user = user_repo.get(interaction.user.id)

        embed = DashboardEmbed(interaction, user)
        view = DashboardView(user)

        await interaction.response.send_message(
            embed=embed,
            view=view,
        )


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Dashboard(bot))
