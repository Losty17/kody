from random import shuffle

from discord import ButtonStyle, Interaction, User
from discord.ui import Button, View, button
from i18n import t
from kody.db.models import Question, User
from kody.db.repositories import QuestionRepository, UserRepository
from kody.modules.dashboard.quests import QuestEmbed
from kody.utils import find_child


class QuestView(View):
    def __init__(self, user: User, quest: Question):
        super().__init__(timeout=60)
        self.user = user

        answers = quest.answers
        right_ans = answers[0]
        shuffle(answers)

        for answer in answers:
            self.add_item(self.QuestionButton(
                answer,
                quest.node.name,
                right_ans,
                user
            ))

        self.new_quest_button = find_child(self, "new")
        self.new_quest_button.label = t(
            "questions.new_quest", count=user.quest_pool)

        self.go_back_button = find_child(self, "back")
        self.go_back_button.label = t("votes.back")

    @button(
        row=1,
        emoji="🏠",
        disabled=True,
        custom_id="back",
        style=ButtonStyle.gray,
        label=t("votes.back"),
    )
    async def _go_back(self, i: Interaction, button: Button):
        from kody.modules.dashboard.home import DashboardEmbed, DashboardView

        return await i.response.edit_message(
            embed=DashboardEmbed(i.user, self.user),
            view=DashboardView(self.user)
        )

    @button(
        row=1,
        emoji="📚",
        disabled=True,
        custom_id="new",
        style=ButtonStyle.gray,
        label=t("questions.quest"),
    )
    async def _new_quest(self, i: Interaction, button: Button):
        quest_repo = QuestionRepository()
        quest = quest_repo.random()

        self.user.quest_pool -= 1
        UserRepository().save(self.user)

        return await i.response.edit_message(
            embed=QuestEmbed(i.user, self.user, quest),
            view=QuestView(self.user, quest)
        )

    class QuestionButton(Button):
        def __init__(
            self,
            label: str,
            node: str,
            right_ans: str,
            user: User,
        ):
            super().__init__(style=ButtonStyle.grey, label=label)
            self.answer = (label[:75] + '...') if len(label) >= 80 else label
            self.right_answer = right_ans
            self.node = node
            self.user = user

        async def callback(self, interaction: Interaction) -> None:
            embed = interaction.message.embeds[0]

            if self.answer == self.right_answer:
                embed.color = 0x34eb34
                self.style = ButtonStyle.green

                self.user.bits[self.node] += 1

                UserRepository().save(self.user)
            else:
                embed.color = 0xeb3434
                self.style = ButtonStyle.red

            for child in self.view.children:
                child.disabled = True

            back_button = find_child(self.view, "back")
            if back_button:
                back_button.disabled = False

            if self.user.quest_cooldown <= 0:
                new_button = find_child(self.view, "new")
                if new_button:
                    new_button.disabled = False

            await interaction.response.edit_message(
                embed=embed,
                view=self.view
            )
