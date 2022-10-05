from discord import Interaction, Button as DButton
from discord.ui import View
from kody.components.buttons import Button, HomeButton
from kody.db.models import User
from kody.dashboard.inventory import InventoryEmbed
from kody.dashboard.bits import BitsEmbed
from kody.utils import switch_page


class InventoryView(View):
    def __init__(self, user: User):
        super().__init__()
        self.add_item(HomeButton(user))
        self.add_item(Button(
            "🎒",
            "Inventário",
            user,
            "inventory",
            self.__handle_inventory,
            disabled=True,
        ))
        self.add_item(Button(
            "💰",
            "Bits",
            user,
            "bits",
            self.__handle_bits,
        ))

    async def __handle_inventory(self, i: Interaction, user: User, button: DButton):
        switch_page(self, button.custom_id)

        await i.response.edit_message(content="", embed=InventoryEmbed(i.user, user), view=self)

    async def __handle_bits(self, i: Interaction, user: User, button: DButton):
        switch_page(self, button.custom_id)

        await i.response.edit_message(content="", embed=BitsEmbed(i.user, user), view=self)
