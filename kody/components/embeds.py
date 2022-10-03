from datetime import datetime

from discord import Color
from discord import Embed as DEmbed
from discord import Member
from kody.db.models.user import User


class Embed(DEmbed):
    def __init__(self, member: Member, user: User):
        super().__init__(timestamp=datetime.now())
        self.user = user
        self.member = member

        self.color = Color.from_str(user.color)

        self.set_image(url=user.cape)
