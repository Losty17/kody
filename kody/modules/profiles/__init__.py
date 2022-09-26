from typing import Optional

from discord import AllowedMentions, Interaction, Member
from discord.app_commands import command
from discord.ext.commands import Cog

from ..staff import KodyBot
from ..staff.database import db
from .embeds import ProfileEmbed
from .views import ProfileView


class Profiles(Cog):
    def __init__(self, bot: KodyBot) -> None:
        self.bot = bot

    @command(name="profile")
    async def _user_data(self, interaction: Interaction, member: Optional[Member] = None):
        target = member or interaction.user

        embed = ProfileEmbed(interaction.guild.get_member(target.id))
        view = ProfileView()

        await interaction.response.send_message(
            interaction.user.mention,
            embed=embed,
            view=view,
            allowed_mentions=AllowedMentions.none()
        )


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Profiles(bot))
