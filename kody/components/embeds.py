from datetime import datetime

from discord import Color
from discord import Embed as DEmbed
from discord import Member
from kody.db.models.user import User


class Embed(DEmbed):
    def __init__(
        self,
        member: Member,
        user: User, *,
        title: str = None,
        description: str = None,
        color: Color = None,
        image: str = None,
        thumbnail: str = None,
        timestamp: datetime = None,
        author: str = None,
        author_icon: str = None,
        footer: str = None,
        footer_icon: str = None,
    ):
        super().__init__()
        self.user = user
        self.member = member

        self.timestamp = timestamp or datetime.now()

        self.title = title
        self.description = description

        self.color = color or Color.from_str(user.color)

        self.set_image(url=image or user.cape)

        if thumbnail:
            self.set_thumbnail(url=thumbnail)

        if author:
            self.set_author(name=author, icon_url=author_icon)

        if footer:
            self.set_footer(text=footer, icon_url=footer_icon)
