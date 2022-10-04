from __future__ import annotations

from discord import Interaction
from discord.ui import View
from i18n import t
from kody.components import Button, ErrorView
from kody.db.models.user import User
from kody.db.repositories import QuestionRepository
from kody.db.repositories.user_repo import UserRepository
from kody.modules.dashboard.quests import QuestEmbed, QuestView
from kody.modules.dashboard.vote import VoteEmbed, VoteView


class DashboardView(View):
    def __init__(self, user: User):
        super().__init__(timeout=300)
        self.user = user

        for button in self.DashboardButtons.buttons():
            self.add_item(Button(
                button["emoji"],
                t(button["label"]),
                user,
                button["key"],
                button["action"],
                row=button["row"],
            ))

    class DashboardButtons:
        @classmethod
        def buttons(cls):
            return [
                {
                    "key": "profile",
                    "emoji": "👤",
                    "label": "dashboard.profile",
                    "action": cls.__handle_profile,
                    "row": 0
                },
                {
                    "key": "inventory",
                    "emoji": "🎒",
                    "label": "dashboard.inventory",
                    "action": cls.__handle_inventory,
                    "row": 0
                },
                {
                    "key": "badges",
                    "emoji": "🎖️",
                    "label": "dashboard.badges",
                    "action": cls.__handle_badges,
                    "row": 0
                },
                {
                    "key": "quest",
                    "emoji": "📚",
                    "label": "dashboard.quest",
                    "action": cls.__handle_quest,
                    "row": 1
                },
                {
                    "key": "vote",
                    "emoji": "🎟️",
                    "label": "dashboard.vote",
                    "action": cls.__handle_vote,
                    "row": 1
                },
                {
                    "key": "daily",
                    "emoji": "🎴",
                    "label": "dashboard.daily",
                    "action": cls.__handle_daily,
                    "row": 1
                },
                {
                    "key": "shop",
                    "emoji": "💰",
                    "label": "dashboard.shop",
                    "action": cls.__handle_shop,
                    "row": 2
                },
                {
                    "key": "config",
                    "emoji": "⚙️",
                    "label": "dashboard.config",
                    "action": cls.__handle_config,
                    "row": 2
                },
                {
                    "key": "help",
                    "emoji": "❓",
                    "label": "dashboard.help",
                    "action": cls.__handle_help,
                    "row": 2
                },
            ]

        @classmethod
        async def __handle_profile(cls, i: Interaction, user: User, button: Button):
            from kody.modules.dashboard.profile import (ProfileEmbed,
                                                        ProfileView)

            await i.response.edit_message(embed=ProfileEmbed(i.user, user), view=ProfileView(user))

        @classmethod
        async def __handle_inventory(cls, i: Interaction, user: User, button: Button):
            from kody.modules.dashboard.inventory import (InventoryEmbed,
                                                          InventoryView)

            await i.response.edit_message(embed=InventoryEmbed(i.user, user), view=InventoryView(user))

        @classmethod
        async def __handle_badges(cls, i: Interaction, user: User, button: Button):
            pass

        @classmethod
        async def __handle_shop(cls, i: Interaction, user: User, button: Button):
            pass

        @classmethod
        async def __handle_quest(cls, i: Interaction, user: User, button: Button):
            cd = user.quest_cooldown
            quest_repo = QuestionRepository()

            if cd <= 0:
                question = quest_repo.random()

                if question:
                    user.quest_pool -= 1
                    UserRepository().save(user)

                    await i.response.edit_message(
                        embed=QuestEmbed(i.user, user, question),
                        view=QuestView(user, question)
                    )

                else:
                    await i.response.edit_message(
                        content=t("questions.notfound"),
                        embed=None,
                        view=ErrorView(user)
                    )
            else:
                await i.response.edit_message(
                    content=t("questions.cooldown", count=round(cd / 60 / 60)),
                    embed=None,
                    view=ErrorView(user)
                )

        @classmethod
        async def __handle_vote(cls, i: Interaction, user: User, button: Button):
            await i.response.edit_message(embed=VoteEmbed(i.user, user), view=VoteView(user))

        @classmethod
        async def __handle_daily(cls, i: Interaction, user: User, button: Button):
            pass

        @classmethod
        async def __handle_config(cls, i: Interaction, user: User, button: Button):
            from kody.modules.dashboard.config import ConfigEmbed, ConfigView

            await i.response.edit_message(embed=ConfigEmbed(i.user, user), view=ConfigView(user))

        @classmethod
        async def __handle_help(cls, i: Interaction, user: User, button: Button):
            pass
