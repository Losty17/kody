from typing import List

from discord import ButtonStyle, Interaction, User, Color
from discord.ui import Button, View

from ..embed import QuestionEmbed

from ..database import db
from .. import NodeEnum


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
        self.ans = label
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
            db.get_user(interaction.user.id).update_node(self.node)
        else:
            m.color = 0xeb3434
            self.style = ButtonStyle.red
            msg = "incorreta..."

        for btn in self.buttons:
            btn.disabled = True



        await interaction.response.edit_message(content=f"{interaction.user.mention}, sua resposta estava {msg}", embed=m, view=self.view)
