from random import shuffle

from discord import ButtonStyle, Interaction, User
from discord.ui import Button, View, button
from i18n import t
from kody.db.models import Question, User
from kody.db.repositories import QuestionRepository, UserRepository
from kody.modules.dashboard.quests import QuestEmbed
from kody.utils import find_child
from kody.components import Button as KButton


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

        self.add_item(KButton(
            "🏠",
            t("votes.back"),
            user,
            "back",
            self.__handle_back,
            row=1,
            disabled=True
        ))

        self.add_item(KButton(
            "📚",
            t("questions.new_quest", count=user.quest_pool),
            user,
            "new",
            self.__handle_new_quest,
            row=1,
            disabled=True
        ))

    async def __handle_back(self, i: Interaction, user: User, button: Button):
        from kody.modules.dashboard.home import DashboardEmbed, DashboardView

        return await i.response.edit_message(
            embed=DashboardEmbed(i.user, user),
            view=DashboardView(user)
        )

    async def __handle_new_quest(self, i: Interaction, user: User, button: Button):
        quest_repo = QuestionRepository()
        quest = quest_repo.random()

        user.quest_pool -= 1
        UserRepository().save(user)

        return await i.response.edit_message(
            embed=QuestEmbed(i.user, user, quest),
            view=QuestView(user, quest)
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
