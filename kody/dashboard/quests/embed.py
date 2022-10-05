from datetime import datetime

from discord import Member
from kody.components import Embed
from kody.db.mappings import NODE_EMOJIS, NODE_TRANSLATIONS
from kody.db.models import Question, User


class QuestEmbed(Embed):
    def __init__(self, member: Member, user: User, question: Question):
        super().__init__(member, user)
        self.description = question.text
        self.set_author(
            name=f"{NODE_EMOJIS[question.node.name]} {NODE_TRANSLATIONS[question.node.name]}"
        )
