from typing import List

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from . import Base
from .models import *

session = None

class Database():
    def __init__(self) -> None:
        super().__init__()

        Session = sessionmaker(bind=Base.metadata.bind, autocommit=True)
        self.session = Session()

    @classmethod
    def get_instance(self):
        return sessionmaker(bind=Base.metadata.bind, autocommit=True)()

    def sync(self):
        Base.metadata.drop_all()
        Base.metadata.create_all()

    
    def add_question(self, question: Question) -> Question:
        with self.session.begin():
            self.session.add(question)

        return question

    def bulk_add_question(self, questions: List[Question]):
        with self.session.begin():
            self.session.bulk_save_objects(questions)

    def get_question(self, _id: str) -> Question:
        with self.session.begin():
            question = self.session.query(Question).filter_by(id=_id).first()

        return question

    def get_questions(self):
        with self.session.begin():
            questions = self.session.query(Question).all()

        return questions

    def get_random_question(self) -> Question | None:
        with self.session.begin():
            questions = self.session.query(Question).order_by(
                func.random()).limit(1).one_or_none()

        return questions
