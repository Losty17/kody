from random import shuffle
from typing import List

from discord import ButtonStyle, Interaction, User
from discord.ui import Button, View

from ....db import Question
from ...staff.database import db


class QuestionUi(View):
    def __init__(self, question: Question, *, author: User):
        super().__init__(timeout=60)

        answers = question.get_answers()
        right_ans = question.right_ans
        shuffle(answers)

        btns = []
        for i in answers:
            if i:
                btns.append(QuestionButton(
                    i, question.node.name, right_ans, btns, author=author))

        for btn in btns:
            self.add_item(btn)


class QuestionButton(Button):
    def __init__(
        self,
        label: str,
        node: str,
        right_ans: str,
        buttons: List[Button],
        *, author: User, style: ButtonStyle = ButtonStyle.grey
    ):
        super().__init__(style=style, label=label)
        self.ans = (label[:76] + '...') if len(label) > 80 else label
        self.right_ans = right_ans
        self.buttons = buttons
        self.node = node
        self.author = author

    async def callback(self, interaction: Interaction) -> None:
        m = interaction.message.embeds[0]

        if self.ans == self.right_ans:
            m.color = 0x34eb34
            self.style = ButtonStyle.green
            msg = "correta!"
            db.get_user(interaction.user.id).increase_node(self.node)
        else:
            m.color = 0xeb3434
            self.style = ButtonStyle.red
            msg = "incorreta..."

        for btn in self.buttons:
            btn.disabled = True

        await interaction.response.edit_message(content=f"{interaction.user.mention}, sua resposta estava {msg}", embed=m, view=self.view)
