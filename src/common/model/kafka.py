import time
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from common.config import SERVICE_NAME

T = TypeVar("T")


class BaseEvent(BaseModel, Generic[T]):
    service: str = SERVICE_NAME
    crid: str | None = None
    topic: str
    payload: T
    ts: float = Field(default_factory=lambda: time.time())
