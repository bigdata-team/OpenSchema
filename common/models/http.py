from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..utils import Now


T = TypeVar("T")


class ResponseModel(BaseModel):
    message: str
    detail: str = None
    timestamp: str = Field(default_factory=lambda: Now().iso)


class DataResponseModel(ResponseModel, Generic[T]):
    data: T


def create_response(message, detail=None, data=None, code=200):

    if data:
        content = DataResponseModel(message=message, detail=detail, data=data)
    else:
        content = ResponseModel(message=message, detail=detail)
    content = jsonable_encoder(content)
    return JSONResponse(content, status_code=code)
