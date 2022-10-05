from discord import Member
from i18n import t
from kody.components import Embed
from kody.dashboard.config.buttons import BUTTONS
from kody.db.models import User


class ConfigEmbed(Embed):
    def __init__(self, member: Member, user: User):
        super().__init__(member, user)

        self.title = f"⚙️ {t('config.title')}"

        def get_status(key):
            return t("common.enabled") if user.preferences[key] else t("common.disabled")

        for button in BUTTONS:
            self.add_field(
                name=t(f"config.{button}"),
                value=get_status(button)
            )
