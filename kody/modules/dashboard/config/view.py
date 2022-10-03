from discord import ButtonStyle, Interaction
from discord.ui import View
from kody.components import Button, HomeButton
from kody.db.models import User
from kody.db.repositories import UserRepository
from kody.modules.dashboard.config.embed import ConfigEmbed


class ConfigView(View):
    def __init__(self, user: User):
        super().__init__(timeout=300)

        self.add_item(HomeButton(user, row=4))

        self.add_item(Button(
            "🏷️",
            "Esconder Legendas",
            user,
            "hide_labels",
            self.__handle_hide_labels,
            row=0,
            style=ButtonStyle.green if user.preferences["hide_labels"] else ButtonStyle.red
        ))

    async def __handle_hide_labels(self, i: Interaction, user: User, button: Button):
        user.preferences["hide_labels"] = not user.preferences["hide_labels"]
        UserRepository().save(user)

        await i.response.edit_message(embed=ConfigEmbed(i.user, user), view=ConfigView(user))
