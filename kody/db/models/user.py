from __future__ import annotations

from datetime import datetime
from typing import Dict

from sqlalchemy import BigInteger, Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from .. import Base
from ..enums import NodeEnum, VipEnum


class User(Base):
    __tablename__ = 'users'

    # Basic data
    id: int = Column(BigInteger, primary_key=True)
    _bits: str = Column('bits', String(64), server_default='0;0;0;0;0;0;0;0')
    vip: VipEnum = Column(Enum(VipEnum), server_default=VipEnum.none.name)

    # Cooldowns
    last_vote: datetime = Column(DateTime(timezone=True))
    last_question: datetime = Column(DateTime(timezone=True))

    # Profile
    bio: str = Column(String(200), server_default='Isso aqui está tão vazio...')
    color: str = Column(String(9), server_default='#ffffff')
    badges: str = Column(String(255), server_default='')

    # Statistics
    quests_seen: int = Column(Integer, server_default='0')
    quests_answered: int = Column(Integer, server_default='0')
    quests_right: int = Column(Integer, server_default='0')

    # Default fields
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True), onupdate=func.now())

    # Declaring before so we can initialize when the User object
    # is fully loaded, avoiding issues with None pointers.
    __bit_dict = None
        
    def __repr__(self) -> str:
        return f"<User id={self.id}>"

    @property
    def bits(self):
        self.__bit_dict = self.__bit_dict or self.BitDict(self)
        return self.__bit_dict

    class BitDict(dict):
        dict: Dict[str, int] = {}
        
        def __init__(self, user: User):
            self.user = user
            data = user._bits.split(';')
            
            for i, node in enumerate(NodeEnum):
                self[node.name] = int(data[i])

        def __setitem__(self, key: str, item: int):
            self.dict[key] = item

            self.user._bits = ';'.join(str(i) for i in self.dict.values())

        def __getitem__(self, key: str):
            return self.dict[key]
            
        def __str__(self):
            return str(self.dict)

        def __repr__(self):
            return repr(self.dict)

        def __len__(self):
            return len(self.dict)

        def __delitem__(self, key: str):
            return

        def clear(self):
            return

        def copy(self):
            return self.dict.copy()

        def has_key(self, k: str):
            return k in self.dict

        def update(self, *args, **kwargs):
            return self.dict.update(*args, **kwargs)

        def keys(self):
            return self.dict.keys()

        def values(self):
            return self.dict.values()

        def items(self):
            return self.dict.items()

        def pop(self, *args):
            return

        def __cmp__(self, dict_: Dict):
            return self.__cmp__(self.dict, dict_)

        def __contains__(self, item):
            return item in self.dict
