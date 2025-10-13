from datetime import datetime, timezone
from typing import Generic, TypeVar, overload

from fastapi.responses import Response
from pydantic import BaseModel, Field

T = TypeVar("T")


class Body(BaseModel):
    message: str | None
    detail: str | None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DataBody(Body, Generic[T]):
    data: T


@overload
def create_response_model(message: str = "Ok", detail: str | None = None) -> Body: ...
@overload
def create_response_model(
    message: str = "Ok", detail: str | None = None, data: T = ...
) -> DataBody[T]: ...


def create_response_model(
    message: str = "Ok", detail: str | None = None, data: T | None = None
):
    if data is not None:
        return DataBody(message=message, detail=detail, data=data)
    return Body(message=message, detail=detail)


def create_response(
    message: str = "Ok", detail: str = None, data: T = None, code: int = 200
):

    content = create_response_model(message=message, detail=detail, data=data)

    return Response(content.model_dump_json(), status_code=code)
