from __future__ import annotations

from typing import Awaitable, Callable

from discord import ButtonStyle, Interaction
from discord.ui import Button, View
from i18n import t
from kody.db.models.user import User
from kody.modules.dashboard.vote import VoteEmbed, VoteView
from kody.modules.profiles.embeds import ProfileEmbed


class DashboardView(View):
    def __init__(self, user: User):
        super().__init__(timeout=300)
        self.user = user

        for button in self.DashboardButtons.buttons():
            self.add_item(self.DashboardButton(
                button["emoji"],
                t(button["label"]),
                user,
                button["key"],
                button["action"],
                button["row"],
            ))

    class DashboardButton(Button):
        def __init__(
            self,
            emoji: str,
            label: str,
            user: User,
            key: str,
            callback: Callable[[Interaction, User], Awaitable[None]],
            row: int = 0
        ):
            super().__init__(
                style=ButtonStyle.gray,
                emoji=emoji,
                label=label,
                row=row,
                custom_id=key
            )

            self.action = callback
            self.user = user

        async def callback(self, interaction: Interaction):
            if (interaction.user.id != self.user.id):
                return

            return await self.action(interaction, self.user)

    class DashboardButtons:

        @classmethod
        def buttons(self):
            return [
                {
                    "key": "profile",
                    "emoji": "👤",
                    "label": "dashboard.profile",
                    "action": self.__handle_profile,
                    "row": 0
                },
                {
                    "key": "inventory",
                    "emoji": "🎒",
                    "label": "dashboard.inventory",
                    "action": self.__handle_inventory,
                    "row": 0
                },
                {
                    "key": "badges",
                    "emoji": "🎖️",
                    "label": "dashboard.badges",
                    "action": self.__handle_badges,
                    "row": 0
                },
                {
                    "key": "shop",
                    "emoji": "💰",
                    "label": "dashboard.shop",
                    "action": self.__handle_shop,
                    "row": 0
                },
                {
                    "key": "quest",
                    "emoji": "📚",
                    "label": "dashboard.quest",
                    "action": self.__handle_quest,
                    "row": 1
                },
                {
                    "key": "vote",
                    "emoji": "🎟️",
                    "label": "dashboard.vote",
                    "action": self.__handle_vote,
                    "row": 1
                },
                {
                    "key": "daily",
                    "emoji": "🎴",
                    "label": "dashboard.daily",
                    "action": self.__handle_daily,
                    "row": 1
                },
                {
                    "key": "help",
                    "emoji": "❓",
                    "label": "dashboard.help",
                    "action": self.__handle_help,
                    "row": 1
                },
            ]

        @classmethod
        async def __handle_profile(self, i: Interaction, user: User):
            pass
            # await i.response.edit_message(embed=ProfileEmbed(i.user), view=ProfileView())

        @classmethod
        async def __handle_inventory(self, i: Interaction, user: User):
            pass

        @classmethod
        async def __handle_badges(self, i: Interaction, user: User):
            pass

        @classmethod
        async def __handle_shop(self, i: Interaction, user: User):
            pass

        @classmethod
        async def __handle_quest(self, i: Interaction, user: User):
            pass

        @classmethod
        async def __handle_vote(self, i: Interaction, user: User):
            await i.response.edit_message(embed=VoteEmbed(user), view=VoteView(user))

        @classmethod
        async def __handle_daily(self, i: Interaction, user: User):
            pass

        @classmethod
        async def __handle_help(self, i: Interaction, user: User):
            pass
