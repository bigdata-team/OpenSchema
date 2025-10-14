from pydantic import Field

from common.model.sql import BaseOrm
from common.util.random import generate_name


class User(BaseOrm, table=True):
    name: str = Field(default_factory=generate_name)
