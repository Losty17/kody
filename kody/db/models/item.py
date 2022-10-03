from kody.db import Base
from sqlalchemy import BigInteger, Column, ForeignKey, Integer


class Item(Base):
    __tablename__ = 'items'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    _type: int = Column(Integer, nullable=False)
    amount: int = Column(Integer, nullable=False)
    user_id: int = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Item(owner={self.user_id})"

    @property
    def name(self) -> str:
        return

    @property
    def emoji(self) -> str:
        return

    @property
    def description(self) -> str:
        return

    @property
    def value(self) -> int:
        return

    @property
    def rarity(self) -> str:
        return

    @property
    def type(self) -> str:
        return
