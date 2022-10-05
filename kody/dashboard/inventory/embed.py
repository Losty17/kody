from discord import Color, Member
from kody.components import Embed
from kody.db.models.user import User
from kody.db.repositories import ItemRepository


class InventoryEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        item_repo = ItemRepository()
        items = item_repo.all(member.id)

        item_list = "\n".join(
            f"🔹 {item.amount} · {item.id} · `{item.id}`" for item in items)

        self.title = "🎒 Inventário"
        self.description = f"Inventário de {member.mention}\n\n{item_list}"
