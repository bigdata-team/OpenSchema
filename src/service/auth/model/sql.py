from sqlmodel import Field

from common.model.sql import BaseOrm
from common.util.random import generate_name


class User(BaseOrm, table=True):
    name: str | None = Field(default_factory=generate_name)
    email: str
    hashed_password: str | None = None  # NULL 가능하게 변경
    bio: str | None = None
    role: str = Field(default="user")
    idp_cd: str | None = None
    picture: str | None = None
