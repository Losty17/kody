from __future__ import annotations

from discord.ui import View
from i18n import t
from kody.components import KodyButton
from kody.db.models.user import User
from kody.dashboard.buttons import BUTTONS


class DashboardView(View):
    def __init__(self, user: User):
        super().__init__(timeout=300)

        for button in BUTTONS:
            self.add_item(KodyButton(
                button["emoji"],
                t(button["label"]),
                user,
                button["key"],
                button["action"],
                row=button["row"],
                disabled=button.get("disabled", False),
            ))
