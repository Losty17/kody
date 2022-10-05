from __future__ import annotations

from discord import ButtonStyle, Interaction
from i18n import t
from kody.db.models import User

from .button import KodyButton


class HomeButton(KodyButton):
    def __init__(self, user: User, *, row: int = 0, disabled: bool = False, style: ButtonStyle = ButtonStyle.gray):
        super().__init__(
            emoji="🏠",
            label=t("common.home"),
            user=user,
            key="back",
            callback=self.__handle_go_back,
            disabled=disabled,
            row=row,
            style=style
        )

    async def __handle_go_back(self, i: Interaction, user: User, button: KodyButton):
        from kody.dashboard import DashboardEmbed, DashboardView

        await i.response.edit_message(content="", embed=DashboardEmbed(i.user, user), view=DashboardView(user))
