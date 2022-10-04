from __future__ import annotations

from typing import Awaitable, Callable

from discord import ButtonStyle, Interaction, ui
from i18n import t
from kody.db.models import User


class Button(ui.Button):
    def __init__(
        self,
        emoji: str,
        label: str,
        user: User,
        key: str,
        callback: Callable[[Interaction, User, Button], Awaitable[None]],
        disabled: bool = False,
        row: int = 0,
        style: ButtonStyle = ButtonStyle.gray
    ):
        super().__init__(
            style=style,
            emoji=emoji,
            row=row,
            disabled=disabled,
            custom_id=key
        )

        if (not user.preferences['hide_labels']):
            self.label = label

        self.action = callback
        self.user = user

    async def callback(self, i: Interaction):
        if (i.user.id != self.user.id):
            return

        return await self.action(i, self.user, self)


class HomeButton(Button):
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

    async def __handle_go_back(self, i: Interaction, user: User, button: Button):
        from kody.modules.dashboard.home import DashboardEmbed, DashboardView

        await i.response.edit_message(content="", embed=DashboardEmbed(i.user, user), view=DashboardView(user))
