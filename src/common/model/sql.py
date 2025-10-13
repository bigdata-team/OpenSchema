from datetime import datetime

from sqlmodel import Field, SQLModel

from common.config import SERVICE_DB_SCHEMA
from common.util.random import generate_id


class BaseOrm(SQLModel):
    __table_args__ = {"schema": SERVICE_DB_SCHEMA or "public"}

    id: str = Field(default_factory=generate_id, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime | None = Field(default=None)
