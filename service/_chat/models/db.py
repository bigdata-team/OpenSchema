from common.models.db import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text


class History(Base):
    user_id = Column(Text)
    service_id = Column(Text)
    model_name = Column(Text)
    url = Column(Text)
    request = Column(Text)
    response = Column(Text)
    tokens = Column(Integer)
