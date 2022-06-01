from datetime import datetime

from .question import Question
from .user import User
from sqlalchemy import *
from sqlalchemy.sql import func
from .enums import *
from .mappings import *
from .....db import Base


class Vip(Base):
    __tablename__ = "vips"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(4), nullable=False)
    image: str = Column(String(100))
    emoji: str = Column(String(50))
    description: str = Column(String(80))


class Node(Base):
    __tablename__ = "nodes"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(8), nullable=False)
    image: str = Column(String(100))
    emoji: str = Column(String(50))
    description: str = Column(String(80))


class _User(Base):
    __tablename__ = "users"
    id: int = Column(BigInteger, primary_key=True)
    ref_vip: int = Column(Integer, ForeignKey("vips.id"), index=True)

    streak: int = Column(Integer, server_default="0")
    last_vote: datetime = Column(DateTime)
    last_daily: datetime = Column(DateTime)
    last_question: datetime = Column(DateTime)

    dt_created: datetime = Column(
        DateTime, server_default=func.now())


class UserBit(Base):
    __tablename__ = "user_bits"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ref_user: int = Column(BigInteger, ForeignKey("users.id"), index=True)
    ref_node: int = Column(Integer, ForeignKey("nodes.id"), index=True)
    qty: int = Column(Integer, server_default="0")


class _Question(Base):
    __tablename__ = "questions"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ref_node: int = Column(Integer, ForeignKey("nodes.id"), index=True)
    text: str = Column(String(200), nullable=False)
    explanation: str = Column(String(200))
    right_ans: str = Column(String(50), nullable=False)
    fst_ans: str = Column(String(50), nullable=False)
    snd_ans: str = Column(String(50))
    thd_ans: str = Column(String(50))


class Item(Base):
    __tablename__ = "items"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(30), nullable=False)
    image: str = Column(String(100))
    emoji: str = Column(String(50))
    description: str = Column(String(80))


class UserInventory(Base):
    __tablename__ = "user_inventory"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ref_user: int = Column(BigInteger, ForeignKey("users.id"), index=True)
    ref_item: int = Column(Integer, ForeignKey("items.id"), index=True)
    qty: int = Column(Integer, server_default="0")


class Badge(Base):
    __tablename__ = "badges"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(30), nullable=False)
    image: str = Column(String(100))
    emoji: str = Column(String(50))


class UserBadge(Base):
    __tablename__ = "user_badges"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ref_user: int = Column(BigInteger, ForeignKey("users.id"), index=True)
    ref_badge: int = Column(Integer, ForeignKey("badges.id"), index=True)

    __table_args__ = (
        UniqueConstraint('ref_user', 'ref_badge', name='u_user_badge'),
    )


class SocialType(Base):
    __tablename__ = "social_types"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(20), nullable=False)
    base_url: str = Column(String(50), nullable=False)


class UserSocial(Base):
    __tablename__ = "user_socials"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ref_user: int = Column(BigInteger, ForeignKey("users.id"), index=True)
    ref_social_type: int = Column(Integer, ForeignKey("social_types.id"))
    username: str = Column(String(20), nullable=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    ref_user: int = Column(BigInteger, ForeignKey("users.id"), index=True)
    featured_badge: int = Column(Integer, ForeignKey("badges.id"))
    nickname: str = Column(String(30), nullable=False)
    bio: str = Column(String(200))
    status: str = Column(String(50))
    emoji: str = Column(String(50))
