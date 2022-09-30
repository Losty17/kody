from discord import Interaction, app_commands

from kody.db.models import User
from kody.db.repositories import UserRepository


class CommandTree(app_commands.CommandTree):
    """ Custom command tree to override interaction checks """
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        user_repo = UserRepository()
        user = user_repo.get(interaction.user.id)
        
        if not user:
            user_repo.add(User(id=interaction.user.id))

        return await super().interaction_check(interaction)
