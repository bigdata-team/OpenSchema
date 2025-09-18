from sqlalchemy import Boolean, Column, DateTime, Integer, Text, String

from common.models.db import Base


class Message(Base):
    conversation_id = Column(Text, nullable=False)
    parent_id = Column(Text, nullable=True, default=None)
    role = Column(Text)
    content = Column(Text)


class Conversation(Base):
    user_id = Column(Text)
    title = Column(Text)
