from os import getenv, listdir, path
from pathlib import Path
from traceback import print_exc
from typing import List

from discord import Intents, Object
from discord.ext import commands

from .extensions import *

guilds = [
    Object(id=getenv("KODY")),
]


class KodyBot(commands.Bot):
    package = 'kody'
    ext_dir = 'extensions'
    root_dir = Path(__file__).parent.resolve()

    def __init__(self, command_prefix: str, *, intents: Intents, application_id: int, owner_id: int) -> None:
        super().__init__(
            command_prefix,
            intents=intents,
            application_id=application_id,
        )

        self.owner_id = int(owner_id)

        self.ext = self.get_extensions(self.ext_dir)

        self.glds = guilds

    async def setup_hook(self) -> None:
        await self.load_modules(self.ext)
        await self.sync()
        # await self._clear_global_commands()
        # await self._global_sync()

    async def load_modules(self, extensions: List[str]) -> None:
        """Loads the specified extensions

        Args:
            extensions (List[str]): the list of extensions
        """
        for e in extensions:
            try:
                print(f"Loading: {self.package}{e}...", end=' ')
                await self.load_extension(e, package=self.package)
                print('Ok!')
            except Exception as ex:
                print(f"Failed.")
                print_exc(ex)

    def get_extensions(self, directory: str) -> List[str]:
        """Get the bot's extensions from the specified directory

        Args:
            directory (str): extensions directory
        Returns:
            List[str]: a list containing all the extensions
        """
        file_list = listdir(
            path.join(
                self.root_dir,
                directory
            )
        )

        return [f'.{directory}.{e}' for e in file_list if not e.endswith('__') and not e.endswith('.md')]

    async def sync(self) -> None:
        """ Sync the commands to the specified guilds """
        print('\nSyncing commands...', end=' ')
        for g in self.glds:
            self.tree.copy_global_to(guild=g)
            await self.tree.sync(guild=g)
        print('Ok!')

    async def _global_sync(self) -> None:
        """ Sync commands globally """
        print('\nSyncing commands globally...')

        for g in self.glds:
            print('\nClearing guild commands', end=' ')
            print(f'from: {g.id}', end=' ')
            self.tree.clear_commands(guild=g)
            print('Ok!', end=' Syncing... ')
            await self.tree.sync(guild=g)
            print('Ok!', end=' ')

        print('\nSyncing...')
        await self.tree.sync()
        print('Done!')

    async def _clear_global_commands(self) -> None:
        print('\nClearing global commands...', end=' ')
        self.tree.clear_commands(guild=None)
        print('Ok!')
        print('Syncing...', end=' ')
        await self.tree.sync(guild=None)
        print('Ok!')
