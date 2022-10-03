from datetime import datetime, timedelta
from os import getenv

from discord import Interaction, app_commands

from ..db.models import User, VipEnum
from ..db.repositories import UserRepository


def is_owner():
    def predicate(interaction: Interaction) -> bool:
        return interaction.user.id in [int(_id) for _id in getenv("OWNER_ID").split(",")]
    return app_commands.check(predicate)


def ensure_user_created():
    def predicate(interaction: Interaction) -> bool:
        user_repo = UserRepository()
        user = user_repo.get(interaction.user.id)

        if not user:
            user_repo.add(User(id=interaction.user.id))

        return True
    return app_commands.check(predicate)


def check_cooldown():
    def predicate(interaction: Interaction) -> bool:
        user_repo = UserRepository()
        user = user_repo.get(interaction.user.id)

        if user is None or user.last_question is None:
            return True

        diff: timedelta = datetime.now() - user.last_question
        match user.vip:
            case VipEnum.mega:
                cd = 60 * 60 * 10

            case VipEnum.giga:
                cd = 60 * 60 * 8

            case VipEnum.tera:
                cd = 60 * 60 * 6

            case VipEnum.none:
                cd = 60 * 60 * 12

        if diff.total_seconds() >= cd:
            return True
        else:
            retry_after = (timedelta(seconds=cd) - diff).total_seconds()
            raise app_commands.CommandOnCooldown(cd, retry_after)
    return app_commands.check(predicate)


def is_staff():
    def predicate(interaction: Interaction) -> bool:
        staff_ids = [int(_id) for _id in getenv("OWNER_ID").split(",")]
        return interaction.user.id in staff_ids
    return app_commands.check(predicate)
