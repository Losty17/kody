from datetime import datetime

from discord import Interaction
from discord.app_commands import CommandOnCooldown, command
from discord.ext.commands import Cog

from ..staff import KodyBot
from ..staff.checks import check_cooldown, ensure_user_created
from ..staff.database import db
from .embeds import QuestionEmbed
from .views import QuestionUi


class Questions(Cog):
    def __init__(self, bot: KodyBot) -> None:
        self.bot = bot

    @command(name="quest")
    @check_cooldown(db)
    @ensure_user_created(db)
    async def _question_command(self, interaction: Interaction):
        """ Responda uma perguntinha! """
        # Set the cooldown for the user
        await interaction.response.defer(ephemeral=True, thinking=True)

        user = db.get_user(interaction.user.id)
        user.last_question = datetime.utcnow()

        question = db.get_random_question()

        if question:
            question_embed = QuestionEmbed(question)

            await interaction.followup.send(
                f"{interaction.user.mention}",
                embed=question_embed,
                view=QuestionUi(question, author=interaction.user)
            )
        else:
            await interaction.followup.send("Ocorreu um erro ao procurar uma questão.", ephemeral=True)

    @_question_command.error
    async def _on_question_error(self, interaction: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cd = error.retry_after / 60 / 60

            msg = 'Uma pergunta já foi respondida recentemente. ' + \
                f'Você poderá responder outra pergunta em: {round(cd)}h'

            return await interaction.response.send_message(msg, ephemeral=True)


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Questions(bot))
