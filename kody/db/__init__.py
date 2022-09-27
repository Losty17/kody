from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db_uri = getenv("DATABASE_URI") if getenv(
            "ENVIRONMENT").lower() == "production" else "sqlite:///:memory:"

engine = create_engine(db_uri)

Base = declarative_base()

Base.metadata.bind = engine

from .db import *
