from datetime import datetime
from typing import Generic, TypeVar

from fastapi.responses import Response
from pydantic import BaseModel, Field

from common.util import now

T = TypeVar("T")


class Body(BaseModel):
    message: str | None
    detail: str | None
    timestamp: datetime = Field(default_factory=lambda: now())


class DataBody(Body, Generic[T]):
    data: T


def create_response_model(message: str = "Ok", detail: str = None, data: T = None):

    if data:
        content = DataBody(message=message, detail=detail, data=data)
    else:
        content = Body(message=message, detail=detail)

    return content


def create_response(
    message: str = "Ok", detail: str = None, data: T = None, code: int = 200
):

    content = create_response_model(message=message, detail=detail, data=data)

    return Response(content.model_dump_json(), status_code=code)
