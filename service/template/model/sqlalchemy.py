import os

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, Sequence, Text
from sqlalchemy.orm import declarative_base

from common.model.sqlalchemy import Base


class User(Base):
    __table_args__ = {"schema": os.getenv("SERVICE_NAME", "public")}
    __tablename__ = "users"

    email = Column(Text, nullable=False)
    hashed_password = Column(Text, nullable=False)

    sso_id = Column(Text)
    sso_provider = Column(Text)
