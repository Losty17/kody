from typing import Optional

from discord import Interaction, Member
from discord.app_commands import command
from discord.ext.commands import Cog

from ..staff import KodyBot
from ..staff.database import db


class Profiles(Cog):
    def __init__(self, bot: KodyBot) -> None:
        self.bot = bot

    @command(name="profile")
    async def _user_data(self, interaction: Interaction, member: Optional[Member] = None):
        target = member or interaction.user

        user = db.get_user(target.id)

        data = f'''
id: {user.id}
vip: {user.vip}
last_vote: {user.last_vote}
last_question: {user.last_question}
----
web: {user.web_bits}
data: {user.data_bits}
design: {user.design_bits}
coding: {user.coding_bits}
network: {user.network_bits}
robotics: {user.robotics_bits}
hardware: {user.hardware_bits}
software: {user.software_bits}
        '''

        await interaction.response.send_message(data)


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Profiles(bot))
