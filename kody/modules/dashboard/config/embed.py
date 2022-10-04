from discord import Member
from kody.components import Embed
from kody.db.models import User


class ConfigEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        self.title = "⚙️ Configurações"

        get_status = lambda key: "Ativado" if user.preferences[key] else "Desativado"

        self.add_field(
            name="Esconder Legendas",
            value=get_status("hide_labels")
        )
        self.add_field(name="T", value="AA")
        self.add_field(name="T", value="AA")
        
        self.add_field(name="T", value="AA")
        self.add_field(name="T", value="AA")
        self.add_field(name="T", value="AA")

