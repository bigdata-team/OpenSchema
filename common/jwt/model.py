from pydantic import BaseModel


class TokenPayload(BaseModel):
    pass


class AccessTokenPayload(TokenPayload):
    iss: str
    aud: list[str] | str

    sub: str
    sid: str
    iat: int
    exp: int
    nbf: int
    jti: str


class RefreshTokenPayload(TokenPayload):
    sub: str
    sid: str
    iat: int
    exp: int
    nbf: int
    jti: str


def create_blacklist_value(id) -> str:
    return f"jwt:bl:{id}"
