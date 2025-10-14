import time

from jose import jwt

from common.config import (
    AUDIENCE,
    ISSUER,
    JWT_ACCESS_TOKEN_TTL,
    JWT_ALGORITHM,
    JWT_DECODE_SECRET,
    JWT_ENCODE_SECRET,
    JWT_REFRESH_TOKEN_TTL,
)
from common.model.jwt import AccessTokenPayload, RefreshTokenPayload, TokenPayload
from common.util.random import generate_id


def encode(payload: TokenPayload) -> str:
    return jwt.encode(payload.model_dump(), JWT_ENCODE_SECRET, algorithm=JWT_ALGORITHM)


def decode(token: str, issuer: str = None, audience: str = None) -> TokenPayload:
    d = jwt.decode(
        token,
        JWT_DECODE_SECRET,
        algorithms=[JWT_ALGORITHM],
        issuer=issuer,
        audience=audience,
    )
    if d:
        if "iss" in d and "aud" in d:
            return AccessTokenPayload.model_validate(d)
        else:
            return RefreshTokenPayload.model_validate(d)
    return None


def _verify_token(
    token: str, issuer: str = None, audience: str = None
) -> AccessTokenPayload | RefreshTokenPayload | None:
    try:
        return decode(token, issuer=issuer, audience=audience)
    except Exception:
        return None


def verify_token(
    token: str, issuer: str = ISSUER, audience: str = AUDIENCE
) -> AccessTokenPayload | RefreshTokenPayload:
    access_token = _verify_token(token, issuer=issuer, audience=audience)
    refresh_token = _verify_token(token)
    return access_token or refresh_token or None


def claim_tokens(
    subject: str,
    issuer: str = ISSUER,
    audience: str = AUDIENCE,
    session_id: str | None = None,
) -> tuple[str, str]:
    now = int(time.time())
    session_id = session_id or generate_id()
    access_payload = AccessTokenPayload(
        iss=issuer,
        aud=audience,
        sub=subject,
        sid=session_id,
        iat=now,
        exp=now + JWT_ACCESS_TOKEN_TTL,
        nbf=now,
        jti=generate_id(),
    )

    refresh_payload = RefreshTokenPayload(
        sub=subject,
        sid=session_id,
        iat=now,
        exp=now + JWT_REFRESH_TOKEN_TTL,
        nbf=now,
        jti=generate_id(),
    )

    access_token = encode(access_payload)
    refresh_token = encode(refresh_payload)

    return access_token, refresh_token
