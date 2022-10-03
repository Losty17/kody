from typing import List

from sqlalchemy import Column, Enum, Integer, String

from .. import Base
from ..enums import NodeEnum


class Question(Base):
    __tablename__ = 'questions'
    id: int = Column(Integer, primary_key=True, autoincrement=True)

    node: NodeEnum = Column(Enum(NodeEnum), nullable=False)
    text: str = Column(String(200), nullable=False)

    right_ans: str = Column(String(80), nullable=False)
    first_ans: str = Column(String(80), nullable=False)
    second_ans: str = Column(String(80), server_default='')
    third_ans: str = Column(String(80), server_default='')

    def __repr__(self) -> str:
        return f"<Question id={self.id} node={self.node}>"

    @property
    def answers(self) -> List[str]:
        """Returns the list of answers, with the 0 index being the correct answer

        Returns:
            List[str]: answers
        """
        answers = [self.right_ans, self.first_ans,
                   self.second_ans, self.third_ans]

        return list(filter(None, answers))
