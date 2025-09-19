from sqlalchemy import Boolean, Column, DateTime, Integer, Text, String

from common.models.db import Base


class Project(Base):
    user_id = Column(Text)
    name = Column(Text)

class Course(Base):
    project_id = Column(Text)
    order = Column(Integer)
    name = Column(Text)

class File(Base):
    project_id = Column(Text)
    name = Column(Text)