from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    sid: str
    iat: int
    exp: int
    nbf: int
    jti: str


class AccessTokenPayload(TokenPayload):
    iss: str
    aud: list[str] | str


class RefreshTokenPayload(TokenPayload):
    pass
