from discord import Member
from kody.components import Embed
from kody.db.mappings import NODE_EMOJIS, NODE_TRANSLATIONS
from kody.db.models.user import User


class BitsEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        bits = user.bits
        bit_keys = [key for key in bits.keys()]
        bit_keys.sort(key=lambda i: bits[i])
        bit_keys.reverse()

        bit_list = "\n".join(
            f"{NODE_EMOJIS[bit]} · {bits[bit]} · `{bit} bit` · {NODE_TRANSLATIONS[bit]}" for bit in bit_keys)

        self.title = "Bits"
        self.description = f"Inventário de bits de {member.mention}\n\n{bit_list}"
