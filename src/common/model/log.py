from pydantic import BaseModel, Field
from common.config.const import LOG_LEVEL, SERVICE_NAME
import time


class Log(BaseModel):
    level: str = Field(default=LOG_LEVEL)
    service: str = Field(default=SERVICE_NAME)
    crid: str
    msg: str
    ts: float = Field(default_factory=time.time)
