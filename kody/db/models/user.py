from __future__ import annotations

from datetime import datetime

from kody.db import Base
from kody.db.models.item import Item
from kody.types import Bits, Dict, Preferences, Stats
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'

    # Basic data
    id: int = Column(BigInteger, primary_key=True)
    vip: bool = Column(Boolean, server_default='0')

    # Cooldowns
    last_vote: datetime = Column(DateTime(timezone=True))
    last_daily: datetime = Column(DateTime(timezone=True))
    last_question: datetime = Column(DateTime(timezone=True))
    __quest_pool: int = Column('quest_pool', Integer,
                               server_default='0')

    # Profile
    bio: str = Column(String(180),
                      server_default='Isso aqui está tão vazio...')
    color: str = Column(String(7),
                        server_default='#ffffff')
    cape: str = Column(String(600),
                       server_default='https://i.imgur.com/VMYHFlM.png')
    __badges: str = Column('badges', String(255),
                           server_default='')

    # Default fields
    created_at: datetime = Column(DateTime(timezone=True),
                                  server_default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True),
                                  onupdate=func.now())

    preferences_col: str = Column('preferences', String(255),
                                  server_default='0')
    bits_col: str = Column('bits', String(64),
                           server_default='0;0;0;0;0;0;0;0')
    stats_col: str = Column('stats', String(255),
                            server_default='0;0;0;0;0;0;0;0;0')

    # Declaring before so we c/an initialize when the User object
    # is fully loaded, avoiding issues with None pointers.
    __bits: Bits = None
    __stats: Stats = None
    __preferences: Preferences = None

    def __repr__(self) -> str:
        return f"User(id={self.id})"

    @property
    def stats(self) -> Stats:
        self.__stats = self.__stats or Dict[Stats](self, 'stats_col', Stats)
        return self.__stats

    @property
    def preferences(self) -> Preferences:
        self.__preferences = \
            self.__preferences or \
            Dict[Preferences](
                self,
                'preferences_col',
                Preferences,
                separator=None,
                boolean=True
            )

        return self.__preferences

    @property
    def badges(self):
        return [int(badge) for badge in self.__badges.split(";")]

    @property
    def bits(self) -> Bits:
        self.__bits = self.__bits or Dict[Bits](
            self, 'bits_col', Bits)
        return self.__bits

    @property
    def vote_cooldown(self):
        if not self.last_vote:
            return 0
        else:
            time_diff = (datetime.now() - self.last_vote).total_seconds()
            cd = 60 * 60 * 12

            return cd - time_diff

    @property
    def daily_cooldown(self):
        if not self.last_daily:
            return 0
        else:
            time_diff = (datetime.now() - self.last_daily).total_seconds()
            cd = 60 * 60 * 24

            return cd - time_diff

    @property
    def quest_cooldown(self):
        if not self.last_question:
            self.quest_pool = 5
            return 0

        time_delta = (datetime.now() - self.last_question).total_seconds()
        # cd = 60 * 60 * 4
        cd = 60

        remaining = cd - time_delta

        if remaining <= 0:
            self.quest_pool = 5
            return 0

        if self.quest_pool > 0:
            return 0    

        return remaining

    @property
    def quest_pool(self):
        return self.__quest_pool

    @quest_pool.setter
    def quest_pool(self, value):
        if value == 4:
            self.last_question = datetime.now()

        self.__quest_pool = value

    def add_item(self, _type: int, amount: int = 1):
        from kody.db.repositories.item_repo import ItemRepository

        return ItemRepository().add(
            Item(
                user_id=self.id,
                _type=_type,
                amount=amount
            )
        )
