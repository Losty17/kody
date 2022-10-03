from os import getenv

from discord import Interaction, app_commands

import i18n
from kody.db.models import User
from kody.db.repositories import UserRepository


class CommandTree(app_commands.CommandTree):
    """ Custom command tree to override interaction checks """

    async def interaction_check(self, interaction: Interaction) -> bool:
        user_repo = UserRepository()
        user = user_repo.get(interaction.user.id)

        if not user:
            user = User(
                id=interaction.user.id,
                preferences_col="1" if getenv(
                    "ENVIRONMENT") != "production" else "0",
                vip=True
            )
            user_repo.add(user)

        i18n.set("locale", str(interaction.locale).split("-")[0])

        return await super().interaction_check(interaction)
