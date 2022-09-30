from __future__ import annotations

from discord import Interaction, Member, SelectOption, TextStyle
from discord.ui import Select, View, Modal, TextInput
from kody.db.repositories.user_repo import UserRepository
from kody.modules.profiles.embeds import BitInventoryEmbed, ProfileEmbed

from re import compile

OPTIONS = {
    "profile": {
        "key": "profile",
        "label": "Perfil",
        "emoji": "👤",
        "description": "Seu perfil público"
    },
    "bits": {
        "key": "bits",
        "label": "Coleção de Bits",
        "emoji": "👜",
        "description": "Sua coleção de Bits"
    },
    "inventory": {
        "key": "inventory",
        "label": "Inventário",
        "emoji": "🧳",
        "description": "Seu inventário"
    },
    "stats": {
        "key": "stats",
        "label": "Estatísticas",
        "emoji": "📑",
        "description": "Suas estatísticas pessoais"
    },
}


class ProfileView(View):
    def __init__(self, target: Member, *, active: str = "profile", old_view: ProfileView = None):
        super().__init__(timeout=600)
        self.target = target
        self.add_item(self.Menu(target, active=active, old_view=old_view))

    class Menu(Select):
        def __init__(self, target: Member, *, active: str, old_view: ProfileView):
            if (active == "profile"):
                OPTIONS["edit"] = {
                    "key": "edit",
                    "label": "Editar",
                    "emoji": "✏️",
                    "description": "Edite seu perfil público"
                }
            elif "edit" in OPTIONS:
                del OPTIONS["edit"]

            super().__init__(
                placeholder="Selecione uma opção...",
                options=[
                    SelectOption(
                        label=opt["label"],
                        description=opt["description"],
                        emoji=opt["emoji"],
                        value=opt["key"],
                        default=opt["key"] == active
                    ) for opt in OPTIONS.values()
                ]
            )

            if (old_view):
                del old_view

            self.target = target

        async def callback(self, interaction: Interaction):
            embed = None
            option = self.values[0]

            match option:
                case "profile":
                    embed = ProfileEmbed(self.target)

                case "bits":
                    embed = BitInventoryEmbed(self.target)

                case "inventory":
                    # TODO: show item list
                    pass

                case "stats":
                    # TODO: show stats
                    pass

                case "edit":
                    return await interaction.response.send_modal(ProfileView.EditProfile(self.view))

                case _:
                    pass

            await interaction.response.edit_message(embed=embed, view=ProfileView(self.target, active=option, old_view=self.view))

    class EditProfile(Modal, title="Editando o seu perfil"):
        bio = TextInput(
            label="Biografia", style=TextStyle.long,
            placeholder="Digite sua biografia",
            min_length=0,
            max_length=180,
            required=False
        )
        cape = TextInput(
            label="Capa do perfil", style=TextStyle.long,
            placeholder="Digite o link da imagem para a capa",
            min_length=0,
            max_length=600,
            required=False
        )
        color = TextInput(
            label="Cor do perfil", style=TextStyle.short,
            placeholder="Digite o código hex da cor (e.g. #ffffff, #a040f0)",
            min_length=0,
            max_length=9,
            required=False
        )

        def __init__(self, view: ProfileView):
            super().__init__(custom_id="edit_profile")
            self.view = view

        async def on_submit(self, interaction: Interaction):
            user_repo = UserRepository()
            user = user_repo.get(interaction.user.id)

            user.bio = self.bio.value if len(self.bio.value) > 0 else user.bio
            user.color = self.color.value if self.color.value.startswith(
                "#") else user.color
            if compile("^(http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$").search(self.cape.value) is not None:
                user.cape = self.cape.value

            user_repo.update(user)

            await interaction.response.edit_message(embed=ProfileEmbed(interaction.user), view=ProfileView(interaction.user, active="profile", old_view=self.view))
