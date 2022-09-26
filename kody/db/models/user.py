from sqlalchemy import BigInteger, Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from .. import Base
from .enums import NodeEnum, VipEnum


class User(Base):
    __tablename__ = 'users'

    # Basic data
    id = Column(BigInteger, primary_key=True)
    __bits = Column('bits', String(64), server_default='0;0;0;0;0;0;0;0')
    vip = Column(Enum(VipEnum), server_default=VipEnum.none.name)

    # Cooldowns
    last_vote = Column(DateTime)
    last_question = Column(DateTime)

    # Profile
    bio = Column(String(200), server_default='Isso aqui está tão vazio...')
    badges = Column(String(255), server_default='')

    # Statistics
    quests_seen = Column(Integer, server_default='0')
    quests_answered = Column(Integer, server_default='0')
    quests_right = Column(Integer, server_default='0')

    # Default fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<User id={self.id}>"

    @property
    def bits(self):
        bits = self.__bits.split(";")
        if len(bits) == len(NodeEnum):
            return {node.name: int(bits[i]) for i, node in enumerate(NodeEnum)}
        else:
            raise Exception("Bit array size doesn't match default node size")

    def increase_node(self, node: NodeEnum):
        bits = self.bits
        bits[node.name] += 1

        self.__bits = ";".join(str(i) for i in bits.values())

    def get_global_xp(self) -> int:
        return sum(self.bits.values())
