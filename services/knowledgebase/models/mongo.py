from typing import Generic, TypeVar
from uuid import uuid4

from pydantic import Field

from common.models.mongo import Base


class PageObject(Base):
    type: str = Field(default="page")

    page: int | None = None
    content: str | None = None


class FileObject(Base):
    type: str = Field(default="file")
    job_id: str | None = None
    job_status: str | None = None

    user_id: str | None = None
    file_name: str | None = None
    file_extension: str | None = None
    content_type: str | None = None
    hash: str | None = None

    pages: list[PageObject] | None = None
