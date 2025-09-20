from typing import Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

from ..utils import Now

T = TypeVar("T")


class Envelope(BaseModel, Generic[T]):
    version: str = "v1"
    payload: T | None = None
    cid: str = Field(default_factory=lambda: uuid4())
    ts: str = Field(default_factory=lambda: Now().iso)


def create_event(payload=None, cid=None):
    if cid:
        e = Envelope(payload=payload, cid=cid)
    else:
        e = Envelope(payload=payload)
    return e.model_dump_json().encode("utf-8")
