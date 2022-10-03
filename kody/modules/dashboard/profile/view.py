from __future__ import annotations

from re import compile

from discord import Interaction, TextStyle
from discord.ui import Modal, TextInput, View
from kody.components import Button
from kody.db.models import User
from kody.db.repositories import UserRepository
from kody.modules.dashboard.home import DashboardEmbed, DashboardView
from kody.modules.dashboard.profile import ProfileEmbed
from kody.utils import find_child, switch_page


class ProfileView(View):
    def __init__(self, user: User):
        super().__init__(timeout=600)

        self.add_item(Button(
            "👤",
            "Perfil",
            user,
            "profile",
            self.__handle_profile,
            disabled=True,
            row=0
        ))

        self.add_item(Button(
            "📑",
            "Estatísticas",
            user,
            "stats",
            self.__handle_stats,
            row=0
        ))

        self.add_item(Button(
            "🏠",
            "Voltar",
            user,
            "back",
            self.__handle_go_back,
            row=1
        ))

        self.add_item(Button(
            "✏️",
            "Editar",
            user,
            "edit",
            self.__handle_edit,
            row=1
        ))

    async def __handle_profile(self, i: Interaction, user: User, button: Button):
        switch_page(self, button.custom_id)

        edit = find_child(self, "edit")
        if not edit:
            self.add_item(Button(
                "✏️",
                "Editar",
                user,
                "edit",
                self.__handle_edit,
                row=1
            ))

        await i.response.edit_message(embed=ProfileEmbed(i.user, user), view=self),

    async def __handle_stats(self, i: Interaction, user: User, button: Button):
        switch_page(self, button.custom_id)

        edit = find_child(self, "edit")
        if edit:
            self.remove_item(edit)

        from kody.modules.dashboard.stats import StatsEmbed
        await i.response.edit_message(embed=StatsEmbed(i.user, user), view=self)

    async def __handle_go_back(self, i: Interaction, user: User, button: Button):
        await i.response.edit_message(embed=DashboardEmbed(i.user, user), view=DashboardView(user))

    async def __handle_edit(self, i: Interaction, user: User, button: Button):
        await i.response.send_modal(self.EditModal(user))

    class EditModal(Modal, title="Editando o seu perfil"):
        def __init__(self, user: User):
            super().__init__(custom_id="edit_profile")
            self.user = user

            self.bio = TextInput(
                label="Biografia", style=TextStyle.paragraph,
                placeholder="Digite sua biografia",
                min_length=0,
                max_length=180,
                required=False
            )
            self.add_item(self.bio)

            if user.vip:
                self.cape = TextInput(
                    label="Capa do perfil", style=TextStyle.short,
                    placeholder="Digite o link da imagem para a capa",
                    min_length=0,
                    max_length=600,
                    required=False
                )
                self.add_item(self.cape)

            self.color = TextInput(
                label="Cor do perfil", style=TextStyle.short,
                placeholder="Digite o código hex da cor (e.g. #ffffff, #a040f0)",
                min_length=0,
                max_length=7,
                required=False
            )
            self.add_item(self.color)

        async def on_submit(self, i: Interaction):
            self.user.bio = \
                self.bio.value if len(self.bio.value) > 0 else self.user.bio

            self.user.color = \
                self.color.value if self.color.value.startswith(
                    "#") else self.user.color

            if self.user.vip and compile(
                "^(http(s)?:\/\/)[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
            ).search(self.cape.value) is not None:
                self.user.cape = self.cape.value

            UserRepository().save(self.user)

            await i.response.edit_message(embed=ProfileEmbed(i.user, self.user), view=ProfileView(self.user))
