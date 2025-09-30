from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from common.models.db import Base


class Conversation(Base):
    user_id = Column(Text)
    name = Column(Text)
