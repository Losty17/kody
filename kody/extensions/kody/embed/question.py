from datetime import datetime
from typing import Any, Optional, Union

from discord import Colour, Embed

from kody.db.models.mappings import NODE_EMOJIS

from .. import Question, NODE_TRANSLATIONS
from .... import bot


class QuestionEmbed(Embed):
    def __init__(self, question: Question, *, color: Optional[Union[int, Colour]] = None):
        super().__init__(
            color=color,
            description=question.text,
            timestamp=datetime.utcnow()
        )
        self.set_author(name=f"{NODE_EMOJIS[question.node.name]} {NODE_TRANSLATIONS[question.node.name]}", icon_url=bot.user.avatar.url)
        # self.set_footer(datetime.utcnow())
