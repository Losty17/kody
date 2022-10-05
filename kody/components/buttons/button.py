from __future__ import annotations

from typing import Awaitable, Callable

from discord import ButtonStyle, Interaction
from discord.ui import Button
from kody.db.models import User


class KodyButton(Button):
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
