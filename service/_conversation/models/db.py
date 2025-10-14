from common.models.db import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text


class Conversation(Base):
    user_id = Column(Text)
    name = Column(Text)
