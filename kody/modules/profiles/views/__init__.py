from enum import Enum
from discord import Interaction, SelectOption, Member
from discord.ui import Select, View

from kody.modules.profiles.embeds import ProfileEmbed, BitInventoryEmbed


class Options(Enum):
    profile = 'profile'
    bits = 'bits'
    edit = 'edit'


class ProfileView(View):
    def __init__(self, target: Member):
        super().__init__(timeout=180)
        self.add_item(self.Menu(target))

    class Menu(Select):
        def __init__(self, target: Member):
            super().__init__(options=[
                SelectOption(label="Perfil", emoji="👤",
                             description="Seu perfil público",
                             value=Options.profile.value),
                SelectOption(label="Editar", emoji="✏️",
                             description="Editar seu perfil",
                             value=Options.edit.value),
                SelectOption(label="Bits", emoji="👜",
                             description="Inventário de Bits",
                             value=Options.bits.value)
            ],
            placeholder="Selecione uma opção...")

            # self.values[0] = Options.profile.value

            self.target = target

        async def callback(self, interaction: Interaction):
            embed = None

            match self.values[0]:
                case Options.profile.value:
                    embed = ProfileEmbed(self.target)

                case Options.bits.value:
                    embed = BitInventoryEmbed(self.target)

                case Options.edit.value:
                    return

                case _:
                    return
            
            await interaction.response.edit_message(embed=embed)