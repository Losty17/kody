from datetime import datetime
from typing import Optional, Union

from discord import Colour, Embed

from ....db import NODE_EMOJIS, NODE_TRANSLATIONS, Question


class QuestionEmbed(Embed):
    def __init__(self, question: Question, *, color: Optional[Union[int, Colour]] = None):
        super().__init__(
            color=color,
            description=question.text,
            timestamp=datetime.utcnow()
        )
        self.set_author(
            name=f"{NODE_EMOJIS[question.node.name]} {NODE_TRANSLATIONS[question.node.name]}"
        )
