from typing import TypedDict

from discord.ui import Item, View
from i18n import t


def find_child(view: View, _id: str) -> Item[View] | None:
    return next((child for child in view.children if getattr(child, "custom_id") == _id), None)


def get_greeting(hour):
    return (
        t("dashboard.morning")
        if 5 <= hour <= 11
        else t("dashboard.afternoon")
        if 12 <= hour <= 18
        else t("dashboard.evening")
    )


def get_keys(dict_: TypedDict):
    return dict_.__annotations__.keys()


def switch_page(view: View, _id: str):
    for child in view.children:
        setattr(child, "disabled", getattr(child, "custom_id") == _id)
