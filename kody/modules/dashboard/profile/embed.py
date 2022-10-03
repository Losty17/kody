from datetime import timezone

from discord import Member
from kody.components import Embed
from kody.db.models import User
from StringProgressBar import progressBar as pb


class ProfileEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        self.title = member.nick or member.name
        self.description = "***Desenvolvedor de Software***\n\n" + user.bio
        self.set_thumbnail(url=member.avatar.url)

        level = round(user.stats["quests_right"] / 64)
        xp = user.stats["quests_right"] - (level * 64)

        bar = pb.filledBar(64, xp if xp > 2 else 2,
                           size=20, line="  ", slider="▰")
        self.add_field(
            name=f"Nível {level}",
            value=f"```{bar[0]}```",
            inline=False
        )

        self.add_field(
            name="Quests",
            value=f'```yaml' +
            f'\nVistas: {user.stats["quests_seen"]}' +
            f'\nRespondidas: {user.stats["quests_answered"]}' +
            f'\nAcertadas: {user.stats["quests_right"]}\n```'
        )

        self.add_field(
            name="Medalhas",
            value="```\n🧑‍💻 Especialista em Software\n🛡️ Chefe de Segurança\n```",
            inline=False
        )

        self.set_footer(text="Criado")
        self.timestamp = user.created_at.replace(
            tzinfo=timezone.utc).astimezone(tz=None)
