from sqlalchemy import Boolean, Column, DateTime, Integer, Text, String

from common.models.db import Base


class History(Base):
    user_id = Column(Text)
    service_name = Column(Text)
    request = Column(Text)
    response = Column(Text)
    tokens = Column(Integer)