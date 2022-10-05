from discord import Interaction
from discord.app_commands import CommandOnCooldown, command, locale_str
from i18n import t
from kody import KodyBot
from kody.db.repositories import QuestionRepository, UserRepository
from kody.modules import BaseCog
from kody.dashboard.quests import QuestEmbed, QuestView


class Questions(BaseCog):
    def __init__(self, bot: KodyBot) -> None:
        super().__init__(bot)

    @command(
        name=locale_str("quest", namespace="commands"),
        description=locale_str("questdesc", namespace="commands")
    )
    async def _question_command(self, i: Interaction):

        # Set the cooldown for the user
        await i.response.defer()

        user_repo = UserRepository()
        user = user_repo.get(i.user.id)

        if user.quest_cooldown <= 0:
            quest_repo = QuestionRepository()
            quest = quest_repo.random()

            user.quest_pool -= 1
            UserRepository().save(user)

            view = QuestView(user, quest)
            view.remove_item(view.new_quest_button)
            view.remove_item(view.go_back_button)

            return await i.followup.send(
                embed=QuestEmbed(i.user, user, quest),
                view=view
            )
        else:
            raise CommandOnCooldown(60 * 60 * 4, user.quest_cooldown)

    @_question_command.error
    async def _on_question_error(self, i: Interaction, error):
        if isinstance(error, CommandOnCooldown):
            cd = error.retry_after

            msg = t("questions.cooldown", count=round(cd / 60 / 60))

            return await i.followup.send(msg)


async def setup(bot: KodyBot) -> None:
    await bot.add_cog(Questions(bot))
