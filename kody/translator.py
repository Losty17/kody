from discord import app_commands, Locale
from discord.app_commands import TranslationContext, locale_str

import i18n


class Translator(app_commands.Translator):
    def __init__(self) -> None:
        super().__init__()

    async def load(self) -> None:
        return await super().load()

    async def translate(self, string: locale_str, locale: Locale, context: TranslationContext) -> str:
        i18n.set("locale", str(locale).split("-")[0])
        ns = string.extras.get("namespace")

        return i18n.t(f'{ns}.{str(string)}') if ns is not None else str(string)
