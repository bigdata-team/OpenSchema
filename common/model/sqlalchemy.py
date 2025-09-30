from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, Sequence
from sqlalchemy.orm import declarative_base

from common.util import now

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    seq = Column(Integer, autoincrement=True)
    created_at = Column(DateTime, default=now())
    updated_at = Column(DateTime, default=now(), onupdate=now())
    deleted_at = Column(DateTime)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
