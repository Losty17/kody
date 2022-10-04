
from discord import ButtonStyle, Interaction
from discord.ui import Button, View, button
from i18n import t
from kody.components.buttons import HomeButton
from kody.db.models.user import User


class VoteView(View):
    def __init__(self, user: User):
        super().__init__(timeout=300)

        self.user = user

        self.add_item(HomeButton(user))

        self.add_item(Button(
            style=ButtonStyle.link,
            label=t("votes.title"),
            url="https://top.gg/bot/852202202000578600"
        ))
