from datetime import datetime
from random import choice

from discord import Color, Embed, Interaction
from i18n import t
from kody.db.models.user import User
from kody.utils import get_greeting


class DashboardEmbed(Embed):
    def __init__(self, interaction: Interaction, user: User):
        super().__init__()

        curr_date = datetime.now()
        emojis = [
            "<:GCHemoji04_wow:1025562850330152991>",
            "<:Blonde_Neko_Scared:1025562793325383682>",
            "<:LutoAraka_Blush:1025562823566311514>",
            "<:raphNhom:674648257321893940>"
        ]

        vote_cd = user.vote_cooldown
        next_vote = t(
            "dashboard.next_cooldown_minutes",
            count=round(vote_cd / 60)
        ) if vote_cd < 60 * 60 else t("dashboard.next_cooldown_hours", count=round(vote_cd / 60 / 60))

        daily_cd = user.daily_cooldown
        next_daily = t(
            "dashboard.next_cooldown_minutes",
            count=round(daily_cd / 60)
        ) if daily_cd < 60 * 60 else t("dashboard.next_cooldown_hours", count=round(daily_cd / 60 / 60))

        quest_cd = user.quest_cooldown
        next_quest = t(
            "dashboard.next_cooldown_minutes",
            count=round(quest_cd / 60)
        )

        msg = f"{get_greeting(curr_date.hour)}, {interaction.user.nick or interaction.user.name}! {choice(emojis)}"

        self.title = msg
        self.timestamp = curr_date
        self.color = Color.from_str(user.color)

        self.add_field(name=f"📚 {t('dashboard.next_quest')}", value=next_quest)
        self.add_field(name=f"🎟️ {t('dashboard.next_vote')}", value=next_vote)
        self.add_field(name=f"🎴 {t('dashboard.next_daily')}", value=next_daily)

        self.set_image(url=user.cape)
