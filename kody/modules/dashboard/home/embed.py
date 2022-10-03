from datetime import datetime
from random import choice

from discord import Emoji, Member, Object
from i18n import t
from kody.components import Embed
from kody.db.models.user import User
from kody.utils import get_greeting
from kody import kody


class DashboardEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        curr_date = datetime.now()
        emojis = [
            "<a:02Dance:880191460639662170>",
            "<:02Pat:924928328077541376>",
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
        ) if quest_cd < 60 * 60 else t("dashboard.next_cooldown_hours", count=round(quest_cd / 60 / 60))

        msg = f"{get_greeting(curr_date.hour)}, {member.nick or member.name}! {choice(emojis)}"

        self.title = msg
        self.timestamp = curr_date

        self.add_field(name=f"📚 {t('dashboard.next_quest')}", value=next_quest)
        self.add_field(name=f"🎟️ {t('dashboard.next_vote')}", value=next_vote)
        self.add_field(name=f"🎴 {t('dashboard.next_daily')}", value=next_daily)
