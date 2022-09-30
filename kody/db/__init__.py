from os import getenv
from typing import List

from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

db_uri = getenv("DATABASE_URI") if getenv(
            "ENVIRONMENT").lower() == "production" else "sqlite:///:memory:"

engine = create_engine(db_uri)

Base = declarative_base()

Base.metadata.bind = engine

from .models import *

class Database():
    def __init__(self) -> None:
        super().__init__()

        Session = sessionmaker(bind=Base.metadata.bind, autocommit=True)
        self.session = Session()

    @classmethod
    def get_instance(self):
        return sessionmaker(bind=Base.metadata.bind, autocommit=True)()
    
    @classmethod
    def sync(self):
        Base.metadata.drop_all()
        Base.metadata.create_all()

