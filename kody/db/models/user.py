from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from .. import Base
from .enums import NodeEnum, VipEnum

class User(Base):
    __tablename__ = 'users'

    # Basic data
    id: int = Column(BigInteger, primary_key=True)
    __bits: str = Column('bits', String(64), server_default='0;0;0;0;0;0;0;0')
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

    def __repr__(self) -> str:
        return f"<User id={self.id}>"

    @property
    def bits(self):
        bits = self.__bits.split(";")
        if len(bits) == len(NodeEnum):
            return {node.name: int(bits[i]) for i, node in enumerate(NodeEnum)}
        else:
            raise Exception("Bit array size doesn't match default node size")

    def increase_node(self, node: NodeEnum, amount: int = 1):
        # TODO: create a class for the dict with custom get and set for nodes
        bits = self.bits
        bits[node.name] += amount

        self.__bits = ";".join(str(i) for i in bits.values())
        self.quests_right += amount

        return self
