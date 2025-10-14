from datetime import datetime, timezone
from typing import Generic, TypeVar, overload

from fastapi.responses import Response
from pydantic import BaseModel, Field

T = TypeVar("T")


class Body(BaseModel):
    detail: str | None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DataBody(Body, Generic[T]):
    data: T | None


@overload
def create_response_model(detail: str | None = None) -> Body: ...
@overload
def create_response_model(detail: str | None = None, data: T = ...) -> DataBody[T]: ...


def create_response_model(detail: str | None = None, data: T | None = None):
    if data is not None:
        return DataBody(detail=detail, data=data)
    return Body(detail=detail)


def create_response(code: int = 200, detail: str = None, data: T = None):

    content = create_response_model(detail=detail, data=data)

    return Response(content.model_dump_json(), status_code=code)
