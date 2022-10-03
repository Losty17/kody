from typing import Optional

from discord import AllowedMentions, Interaction, Member
from discord.app_commands import command, locale_str

from .. import BaseCog
from ..staff import KodyBot


class Profiles(BaseCog):
    def __init__(self, bot: KodyBot) -> None:
        super().__init__(bot)

    @command(
        name=locale_str("profile", namespace="commands"),
        description=locale_str("profiledesc", namespace="commands")
    )
    async def _show_profile(self, interaction: Interaction, member: Optional[Member] = None):
        target = member or interaction.user

        # embed = ProfileEmbed(interaction.guild.get_member(target.id))
        # view = ProfileView(interaction.guild.get_member(target.id))

        await interaction.response.send_message(
            interaction.user.mention,
            # embed=embed,
            # view=view,
            allowed_mentions=AllowedMentions.none()
        )


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Profiles(bot))
