from datetime import datetime, timezone
from uuid import uuid4

from beanie import Document
from pydantic import Field


class Base(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return await super().save(*args, **kwargs)

    async def update(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return await super().update(*args, **kwargs)
