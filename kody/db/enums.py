from enum import Enum


class VipEnum(Enum):
    none = 0
    once = 1
    mega = 2
    giga = 3
    tera = 4


class NodeEnum(Enum):
    __order__: str = 'web data design coding network robotics hardware software'
    web: str = 0
    data: str = 1
    design: str = 2
    coding: str = 3
    network: str = 4
    robotics: str = 5
    hardware: str = 6
    software: str = 7
