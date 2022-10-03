from enum import Enum


class VipEnum(Enum):
    none = 0
    once = 1
    mega = 2
    giga = 3
    tera = 4


class NodeEnum(Enum):
    __order__: str = 'data hard soft net web code shield social'
    data: str = 0
    hard: str = 1
    soft: str = 2
    net: str = 3
    web: str = 4
    code: str = 5
    shield: str = 6
    social: str = 7


class PreferencesEnum(Enum):
    __order__: str = 'language hide_labels'
    language: str = 0
    hide_labels: str = 1
