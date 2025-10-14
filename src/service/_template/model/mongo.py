from pydantic import Field

from common.model.mongo import BaseDocument
from common.util.random import generate_name


class User(BaseDocument):
    name: str = Field(default_factory=generate_name)
