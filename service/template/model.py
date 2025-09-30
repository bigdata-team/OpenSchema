from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, Sequence, Text, Boolean
from sqlalchemy.orm import declarative_base

from common.model.sqlalchemy import Base


class User(Base):
    __tablename__ = "users"
    email = Column(Text, nullable=False)
    hashed_password = Column(Text, nullable=False)

    sso_id = Column(Text)
    sso_provider = Column(Text)
