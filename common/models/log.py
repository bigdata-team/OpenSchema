from pydantic import BaseModel


class Log(BaseModel):
    detail: str = None
    cid: str = None
