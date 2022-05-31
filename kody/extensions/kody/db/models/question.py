from typing import List

from sqlalchemy import Column, DateTime, Enum, Integer, String

from .....db import Base
from .enums import NodeEnum


class Question(Base):
    __tablename__ = 'questions'
    id: int = Column(Integer, primary_key=True, autoincrement=True)

    node: NodeEnum = Column(Enum(NodeEnum), nullable=False)
    text: str = Column(String(200), nullable=False)

    right_ans: str = Column(String(200), nullable=False)
    first_ans: str = Column(String(200), nullable=False)
    second_ans: str = Column(String(200), server_default='')
    third_ans: str = Column(String(200), server_default='')

    def __repr__(self) -> str:
        return f"<Question id={self.id} node={self.node}>"

    def get_answers(self) -> List[str]:
        return [self.right_ans, self.first_ans, self.second_ans, self.third_ans]
