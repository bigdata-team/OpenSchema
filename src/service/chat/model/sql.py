from pydantic import Field

from common.model.sql import BaseOrm
from common.util.random import generate_name


class History(BaseOrm, table=True):
    user_id: str
    service_id: str
    model_name: str
    url: str
    request: str
    response: str
    tokens: int
