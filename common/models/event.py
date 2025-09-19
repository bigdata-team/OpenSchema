from typing import Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

from ..utils import Now

T = TypeVar("T")


class Envelope(BaseModel, Generic[T]):
    version: str = "v1"
    payload: T | None = None
    crid: str = Field(default_factory=lambda: uuid4())
    ts: str = Field(default_factory=lambda: Now().iso)


def create_event(payload=None, crid=None):
    if crid:
        e = Envelope(payload=payload, crid=crid)
    else:
        e = Envelope(payload=payload)
    return e.model_dump_json().encode("utf-8")
