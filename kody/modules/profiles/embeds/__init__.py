from datetime import timezone

from discord import Colour, Embed, Member
from StringProgressBar import progressBar as pb

from ....db.repositories import UserRepository


class ProfileEmbed(Embed):
    def __init__(self, member: Member):
        super().__init__()
        user_repo = UserRepository()
        user = user_repo.get(member.id)

        self.color = Colour.from_str(user.color)

        self.title = member.nick or member.name
        self.description = "***Desenvolvedor de Software***\n\n" + user.bio
        self.set_thumbnail(url=member.avatar.url)

        level = round(user.quests_right / 64)
        xp = user.quests_right - (level * 64)

        bar = pb.filledBar(64, xp if xp > 2 else 2,
                           size=20, line="  ", slider="▰")
        self.add_field(
            name=f"Nível {level}",
            value=f"```{bar[0]}```",
            inline=False
        )

        self.add_field(
            name="Quests",
            value=f'```yaml\nVistas: {user.quests_seen}\nRespondidas: {user.quests_answered}\nAcertadas: {user.quests_right}\n```'
        )

        self.add_field(
            name="Medalhas",
            value="```\n🧑‍💻 Especialista em Software\n🛡️ Chefe de Segurança\n```",
            inline=False
        )

        self.set_image(
            url="https://i.pinimg.com/originals/44/da/a6/44daa6dd16148062fab11d15b5a0f67d.jpg")

        self.set_footer(text="Criado")
        self.timestamp = user.created_at.replace(
            tzinfo=timezone.utc).astimezone(tz=None)
