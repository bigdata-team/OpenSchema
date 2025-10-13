from datetime import datetime

from beanie import Document as _Document
from pydantic import BaseModel, Field

from common.config import SERVICE_DB_SCHEMA
from common.util.random import generate_id


class DocumentRegistry:
    _documents = []

    @classmethod
    def add(cls, subclass):
        cls._documents.append(subclass)

    @classmethod
    def retrieve(cls):
        return cls._documents


class BaseDocument(_Document):
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        DocumentRegistry.add(cls)

    id: str = Field(
        default_factory=generate_id,
        primary_key=True,
        alias="_id",
        serialization_alias="id",
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime | None = Field(default=None)
