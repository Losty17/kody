from discord import Embed, Member
from kody.db.mappings import NODE_EMOJIS, NODE_TRANSLATIONS
from kody.db.repositories import UserRepository


class BitInventoryEmbed(Embed):
    def __init__(self, member: Member):
        super().__init__()
        user_repo = UserRepository()
        user = user_repo.get(member.id)

        bits = user.bits

        bit_keys = [key for key in bits.keys()]
        bit_keys.sort(key=lambda i: bits[i])
        bit_keys.reverse()

        bit_list = "\n".join(f"{NODE_EMOJIS[bit]} · {bits[bit]} · `{bit} bit` · {NODE_TRANSLATIONS[bit]}" for bit in bit_keys)

        self.title = "Bits"
        self.description = f"Inventário de bits de {member.mention}\n\n{bit_list}"
