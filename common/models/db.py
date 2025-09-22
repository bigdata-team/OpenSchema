import os
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    seq = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at = Column(DateTime(timezone=True), default=None, nullable=True)

    @declared_attr
    def __tablename__(cls):
        SERVICE_NAME = os.getenv("SERVICE_NAME", "")
        return SERVICE_NAME + "_" + cls.__name__.lower()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
