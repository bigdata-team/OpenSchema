from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from common.models.db import Base


class Upload(Base):
    user_id = Column(Text)
    service_id = Column(Text)
    file_name = Column(Text)
    file_path = Column(Text, nullable=False)
    is_uploaded = Column(Boolean, default=False)
