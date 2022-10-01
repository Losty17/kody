from .checks import *
from i18n import t


def get_greeting(hour):
    return (
        t("dashboard.monring")
        if 5 <= hour <= 11
        else t("dashboard.afternoon")
        if 12 <= hour <= 18
        else t("dashboard.evening")
    )
