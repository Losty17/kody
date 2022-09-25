from discord import Interaction
from discord.app_commands import Choice, Group, choices, describe
from discord.ext import commands

from ... import kody
from ...kody import KodyBot
from ...utils import is_owner

module_list = [Choice(name=module.split(".")[2], value=module)
               for module in kody.modules]


class Dev(commands.Cog):
    dev = Group(
        name="dev",
        description="Developer commands",
    )

    def __init__(self, bot: KodyBot) -> None:
        self.bot = bot

    @dev.command()
    @describe(module="Module to be loaded")
    @choices(module=module_list)
    @is_owner()
    async def load(self, interaction: Interaction, *, module: str, sync: bool = True):
        """ Load an extension """
        await interaction.response.defer(ephemeral=True)

        fqn = f'{self.bot.package}{module}'

        try:
            self.bot.logger.info(f"Loading extension {fqn}...")
            await self.bot.load_extension(module, package=self.bot.package)
            if sync:
                await self.bot.sync()
        except commands.ExtensionError:
            await interaction.response.send_message(
                f"Não foi possível carregar o módulo `{fqn}`",
                ephemeral=True
            )
        else:
            await interaction.followup.send(f'`{fqn}` foi carregado com sucesso', ephemeral=True)

    @dev.command()
    @describe(module="Module to be unloaded")
    @choices(module=module_list)
    @is_owner()
    async def unload(self, interaction: Interaction, *, module: str, sync: bool = True):
        """ Unload an extension """
        await interaction.response.defer(ephemeral=True)

        fqn = f'{self.bot.package}{module}'

        try:
            self.bot.logger.info(f"Unloading extension {fqn}...")
            await self.bot.unload_extension(module, package=self.bot.package)
            if sync:
                await self.bot.sync()
        except commands.ExtensionError:
            await interaction.response.send_message(
                f"Não foi possível descarregar o módulo `{fqn}`",
                ephemeral=True
            )
        else:
            await interaction.followup.send(f'`{fqn}` foi descarregado com sucesso', ephemeral=True)

    @dev.command()
    @describe(module="Module to be reloaded")
    @choices(module=module_list)
    @is_owner()
    async def reload(self, interaction: Interaction, *, module: str, sync: bool = True):
        """ Reload an extension """
        await interaction.response.defer(ephemeral=True)

        fqn = f'{self.bot.package}{module}'
        try:
            self.bot.logger.info(f"Reloading extension {fqn}...")
            await self.bot.reload_extension(module, package=self.bot.package)
            if sync:
                await self.bot.sync()
        except commands.ExtensionError:
            await interaction.response.send_message(
                f"Não foi possível recarregar o módulo `{fqn}`",
                ephemeral=True
            )
        else:
            await interaction.followup.send(f'`{fqn}` foi recarregado com sucesso', ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))
