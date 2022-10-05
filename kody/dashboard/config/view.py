from math import floor

from discord import ButtonStyle, Interaction
from discord.ui import View
from i18n import t
from kody.components import HomeButton, KodyButton
from kody.dashboard.config.buttons import BUTTONS, EMOJIS
from kody.dashboard.config.embed import ConfigEmbed
from kody.db.models import User
from kody.db.repositories import UserRepository


class ConfigView(View):
    def __init__(self, user: User):
        super().__init__(timeout=300)

        self.add_item(HomeButton(user, row=4))

        for i, button in enumerate(BUTTONS):
            self.add_item(KodyButton(
                EMOJIS[button],
                t(f'config.{button}'),
                user,
                button,
                self.__toggle_setting,
                row=floor(i / 3),
                style=ButtonStyle.green if user.preferences[button] else ButtonStyle.red
            ))

    async def __toggle_setting(self, i: Interaction, user: User, button: KodyButton):
        if button.custom_id in user.preferences:
            user.preferences[button.custom_id] = not user.preferences[button.custom_id]
            UserRepository().save(user)

        await i.response.edit_message(embed=ConfigEmbed(i.user, user), view=ConfigView(user))
