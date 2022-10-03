from discord import ui
from kody.db.models import User
from .buttons import HomeButton


class ErrorView(ui.View):
    def __init__(self, user: User):
        super().__init__(timeout=300)

        self.add_item(HomeButton(user))
