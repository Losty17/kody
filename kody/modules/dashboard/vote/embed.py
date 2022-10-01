
from datetime import datetime

from discord import Color, Embed
from i18n import t
from kody.db.models.user import User


class VoteEmbed(Embed):
    def __init__(self, user: User):
        super().__init__(
            color=Color.from_str(user.color),
            title=t("votes.title"),
            description=t("votes.description"),
            timestamp=datetime.now()
        )
        self.set_image(url=user.cape)
