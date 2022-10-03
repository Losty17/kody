from discord.ui import Button, Select, View
from i18n import t


def find_child(view: View, _id: str) -> Button | Select | None:
    return next((child for child in view.children if child.custom_id == _id), None)


def get_greeting(hour):
    return (
        t("dashboard.monring")
        if 5 <= hour <= 11
        else t("dashboard.afternoon")
        if 12 <= hour <= 18
        else t("dashboard.evening")
    )


def get_keys(dict_):
    return dict_.__annotations__.keys()


def switch_page(view: View, _id: str):
    for child in view.children:
        if child.custom_id == _id:
            child.disabled = True
        else:
            child.disabled = False
