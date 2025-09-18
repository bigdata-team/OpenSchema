from pydantic import BaseModel


class Log(BaseModel):
    detail: str = None
    txid: str = None
