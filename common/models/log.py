from pydantic import BaseModel


class Log(BaseModel):
    detail: str = None
    crid: str = None
