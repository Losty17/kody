
from datetime import datetime

from discord import Member
from i18n import t
from kody.components import Embed
from kody.db.models.user import User


class VoteEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        self.title = f'🎟️ {t("votes.title")}'
        self.description = t("votes.description")
