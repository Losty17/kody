
from typing import List

from sqlalchemy import func

from ..models import Question
from .base_repo import BaseRepo


class QuestionRepository(BaseRepo[Question]):
    def __init__(self) -> None:
        super().__init__()

    def add(self, quest: Question) -> Question:
        with self.session.begin():
            self.session.add(quest)

        return quest

    def add_all(self, quests: List[Question]) -> List[Question]:
        with self.session.begin():
            self.session.bulk_save_objects(quests)

    def get(self, _id: int) -> Question | None:
        with self.session.begin():
            quest = self.session.query(Question).filter_by(id=_id).first()

        return quest

    def all(self) -> List[Question]:
        with self.session.begin():
            quests = self.session.query(Question).all()

        return quests

    def random(self) -> Question | None:
        with self.session.begin():
            questions = self.session.query(Question)\
                                    .order_by(func.random())\
                                    .limit(1).one_or_none()

        return questions

    def remove(self, target: Question) -> bool:
        success = False
        try:
            with self.session.begin():
                self.session.delete(target)

            success = True
        except:
            pass
        finally:
            self.session.close()

        return success

    def save(self, target: Question) -> Question:
        with self.session.begin():
            self.session.merge(target)

        return target
