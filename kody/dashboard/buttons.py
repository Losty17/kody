from discord import Interaction
from i18n import t
from kody.components import ErrorView, KodyButton
from kody.db.models import User
from kody.db.repositories import QuestionRepository, UserRepository


async def handle_profile(i: Interaction, user: User, button: KodyButton):
    from kody.dashboard.profile import ProfileEmbed, ProfileView

    await i.response.edit_message(embed=ProfileEmbed(i.user, user), view=ProfileView(user))


async def handle_inventory(i: Interaction, user: User, button: KodyButton):
    from kody.dashboard.inventory import InventoryEmbed, InventoryView

    await i.response.edit_message(embed=InventoryEmbed(i.user, user), view=InventoryView(user))


async def handle_badges(i: Interaction, user: User, button: KodyButton):
    pass


async def handle_shop(i: Interaction, user: User, button: KodyButton):
    pass


async def handle_quest(i: Interaction, user: User, button: KodyButton):
    from kody.dashboard.quests import QuestEmbed, QuestView

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


async def handle_vote(i: Interaction, user: User, button: KodyButton):
    from kody.dashboard.vote import VoteEmbed, VoteView

    await i.response.edit_message(embed=VoteEmbed(i.user, user), view=VoteView(user))


async def handle_daily(i: Interaction, user: User, button: KodyButton):
    pass


async def handle_config(i: Interaction, user: User, button: KodyButton):
    from kody.dashboard.config import ConfigEmbed, ConfigView

    await i.response.edit_message(embed=ConfigEmbed(i.user, user), view=ConfigView(user))


async def handle_help(i: Interaction, user: User, button: KodyButton):
    pass


BUTTONS = [
    {
        "key": "profile",
        "emoji": "👤",
        "label": "dashboard.profile",
        "action": handle_profile,
        "row": 0
    },
    {
        "key": "inventory",
        "emoji": "🎒",
        "label": "dashboard.inventory",
        "action": handle_inventory,
        "row": 0
    },
    {
        "key": "badges",
        "emoji": "🎖️",
        "label": "dashboard.badges",
        "action": handle_badges,
        "row": 0
    },
    {
        "key": "quest",
        "emoji": "📚",
        "label": "dashboard.quest",
        "action": handle_quest,
        "row": 1
    },
    {
        "key": "vote",
        "emoji": "🎟️",
        "label": "dashboard.vote",
        "action": handle_vote,
        "row": 1
    },
    {
        "key": "daily",
        "emoji": "🎴",
        "label": "dashboard.daily",
        "action": handle_daily,
        "row": 1,
        "disabled": True
    },
    {
        "key": "shop",
        "emoji": "💰",
        "label": "dashboard.shop",
        "action": handle_shop,
        "row": 2,
        "disabled": True
    },
    {
        "key": "config",
        "emoji": "⚙️",
        "label": "dashboard.config",
        "action": handle_config,
        "row": 2
    },
    {
        "key": "help",
        "emoji": "❓",
        "label": "dashboard.help",
        "action": handle_help,
        "row": 2
    },
]
