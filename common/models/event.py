from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from uuid import uuid4

from ..utils import Now


T = TypeVar("T")


class Envelope(BaseModel, Generic[T]):
    version: str = "v1"
    payload: T | None = None
    txid: str = Field(default_factory=lambda: uuid4())
    ts: str = Field(default_factory=lambda: Now().iso)


def create_event(payload=None, txid=None):
    if txid:
        e = Envelope(payload=payload, txid=txid)
    else:
        e = Envelope(payload=payload)
    return e.model_dump_json().encode("utf-8")
