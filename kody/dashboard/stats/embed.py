from discord import Member
from kody.components import Embed
from kody.db.models import User


class StatsEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        stats = user.stats

        quest_stats = [
            f"Quests vistas: `{stats['quests_seen']}`",
            f"Quests respondidas: `{stats['quests_answered']}`",
            f"Quests acertadas: `{stats['quests_right']}`",
            f"Quests erradas: `{stats['quests_answered'] - stats['quests_right'] if stats['quests_answered'] > stats['quests_right'] else 0}`",
            f"Quests ignoradas: `{stats['quests_seen'] - stats['quests_answered']}`",
            f"Última quest vista: {f'<t:{round(user.last_question.timestamp())}:f>' if user.last_question else '`nenhuma`'}",
        ]

        vote_stats = [
            f"Votos totais: `{stats['total_votes']}`",
            f"Votos em sequência: `{stats['vote_streak']}`",
            f"Recorde de votos em sequência: `{stats['max_vote_streak']}`",
            f"Último voto: {f'<t:{round(user.last_vote.timestamp())}: f > ' if user.last_vote else '`nenhuma`'}",
        ]

        daily_stats = [
            f"Diárias totais: `{stats['total_dailies']}`",
            f"Diárias em sequência: `{stats['daily_streak']}`",
            f"Recorde de diárias em sequência: `{stats['max_daily_streak']}`",
            f"Última diária: {f'<t:{round(user.last_daily.timestamp())}: f > ' if user.last_daily else '`nenhuma`'}",
        ]

        self.title = "📑 Estatísticas"
        self.description = f"Estatísticas de {member.mention}"
        self.add_field(
            name="Quests",
            value="\n".join(f"▪️ {stat}" for stat in quest_stats),
            inline=False
        )
        self.add_field(
            name="Votos",
            value="\n".join(f"▪️ {stat}" for stat in vote_stats),
            inline=False
        )
        self.add_field(
            name="Diárias",
            value="\n".join(f"▪️ {stat}" for stat in daily_stats),
            inline=False
        )
