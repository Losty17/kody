from email.policy import default
from enum import Enum
from discord import Interaction, SelectOption, User
from discord.ui import Select, View


class Options(Enum):
    profile = 'profile'
    edit = 'edit'


class ProfileView(View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(self.Menu())

    class Menu(Select):
        def __init__(self):
            super().__init__(options=[
                SelectOption(label="Perfil", emoji="👤",
                             description="Seu perfil público",
                             default=True,
                             value=Options.profile.value),
                SelectOption(label="Editar", emoji="✏️",
                             description="Editar seu perfil",
                             value=Options.edit.value)
            ])

        async def callback(self, interaction: Interaction):
            msg = interaction.message
            option = self.values[0]

            match option:
                case Options.edit.value:
                    await msg.delete()

                case _:
                    await interaction.response.send_message("teste")
