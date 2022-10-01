from datetime import datetime

import i18n
from discord import Interaction
from discord.app_commands import CommandOnCooldown, command, locale_str
from kody.db.repositories import QuestionRepository, UserRepository

from .. import BaseCog
from ..staff import KodyBot
from ..staff.checks import check_cooldown
from .embeds import QuestionEmbed
from .views import QuestionUi


class Questions(BaseCog):
    def __init__(self, bot: KodyBot) -> None:
        super().__init__(bot)

    @command(name=locale_str("commands_quest"))
    @check_cooldown()
    async def _question_command(self, interaction: Interaction):
        """ questions_dropdesc """

        # Set the cooldown for the user
        await interaction.response.defer(ephemeral=True, thinking=True)

        user_repo = UserRepository()
        user = user_repo.get(interaction.user.id)

        user.last_question = datetime.utcnow()

        question = QuestionRepository().random()

        if question:
            question_embed = QuestionEmbed(question)

            await interaction.followup.send(
                f"{interaction.user.mention}",
                embed=question_embed,
                view=QuestionUi(question, author=interaction.user)
            )
        else:
            await interaction.followup.send(i18n.t("questions.notfound"), ephemeral=True)

    @_question_command.error
    async def _on_question_error(self, interaction: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cd = error.retry_after / 60 / 60

            msg = i18n.t("questions.cooldown", count=round(cd))

            return await interaction.response.send_message(msg, ephemeral=True)


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Questions(bot))
