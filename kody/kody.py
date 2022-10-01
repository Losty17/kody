from datetime import datetime
from os import getenv, listdir, path
from pathlib import Path
from typing import List

from discord import Activity, ActivityType, Intents, Object, Status
from discord.ext import commands

from kody.translator import Translator

from .logger import setup_logger
from .tree import CommandTree


class KodyBot(commands.Bot):
    package = 'kody'
    module_dir = 'modules'
    root_dir = Path(__file__).parent.resolve()

    def __init__(self, command_prefix: str, *, intents: Intents, application_id: int, owner_id: int) -> None:
        super().__init__(
            command_prefix,
            intents=intents,
            application_id=application_id,
            status=Status.idle,
            activity=Activity(
                name="cantigas de ninar",
                type=ActivityType.listening
            ),
            tree_cls=CommandTree
        )
        self.owner_id = owner_id

        self.modules = self.get_extensions(self.module_dir)

        self.dev_guilds = [Object(guild)
                           for guild in getenv("GUILDS").split(",")]

        self.logger = setup_logger()

    async def setup_hook(self) -> None:
        await self.load_modules(self.modules)
        # await self._clear_global_commands()
        # await self._global_sync()
        await self.tree.set_translator(Translator())
        await self.sync()

    async def load_modules(self, extensions: List[str]) -> None:
        """Loads the specified extensions

        Args:
            extensions (List[str]): the list of extensions
        """
        for e in extensions:
            try:
                self.logger.info(f"Loading {self.package}{e}")
                await self.load_extension(e, package=self.package)
            except Exception as ex:
                self.logger.exception(f"Failed:")

    def get_extensions(self, directory: str) -> List[str]:
        """Get the bot's extensions from the specified directory

        Args:
            directory (str): extensions directory
        Returns:
            List[str]: a list containing all the extensions
        """
        file_list = listdir(path.join(self.root_dir, directory))

        try:
            file_list.remove("__pycache__")
        except ValueError:
            pass

        return [f'.{directory}.{file}' for file in file_list if not "." in file]

    async def sync(self) -> None:
        """ Sync the commands to the specified guilds """
        self.logger.debug('Syncing commands')
        before = datetime.utcnow()
        for g in self.dev_guilds:
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)

        elapsed = (datetime.utcnow() - before).total_seconds()

        self.logger.debug(
            f"Done! ({f'{round(elapsed, 2)}s' if elapsed > 1 else f'{round(elapsed* 1000)}ms'} elapsed)")

    async def __global_sync(self) -> None:
        """ Sync commands globally """
        self.logger.warn('Syncing commands globally')

        for g in self.dev_guilds:
            self.logger.warn(f'Clearing guild commands from: {g.id}')
            self.tree.clear_commands(guild=g)
            self.logger.warn(f'Syncing commands for: {g.id}')
            await self.tree.sync(guild=g)

        self.logger.warn('Syncing tree')
        await self.tree.sync()

    async def __clear_global_commands(self) -> None:
        self.logger.warn('Clearing global commands')
        self.tree.clear_commands(guild=None)
        self.logger.warn('Syncing global tree')
        await self.tree.sync(guild=None)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
