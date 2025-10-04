import os
import time

from jose import jwt

from common.model.jwt import (AccessTokenPayload, RefreshTokenPayload,
                              TokenPayload)
from common.util.random import get_id

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ENCODE_SECRET = os.getenv("JWT_ENCODE_SECRET", "supersecret!")
JWT_DECODE_SECRET = os.getenv("JWT_DECODE_SECRET", "supersecret!")
JWT_ACCESS_TOKEN_TTL = int(os.getenv("JWT_ACCESS_TOKEN_TTL", 15 * 60))
JWT_REFRESH_TOKEN_TTL = int(os.getenv("JWT_REFRESH_TOKEN_TTL", 7 * 24 * 60 * 60))


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


def _verify_token(token: str, issuer: str = None, audience: str = None) -> TokenPayload:
    try:
        return decode(token, issuer=issuer, audience=audience)
    except Exception:
        return None


def verify_token(
    token: str, issuer: str = "auth.service", audience: str = "service"
) -> AccessTokenPayload | RefreshTokenPayload:
    access_token = _verify_token(token, issuer=issuer, audience=audience)
    refresh_token = _verify_token(token)
    return access_token or refresh_token or None


def claim_tokens(
    subject: str,
    issuer: str = "auth.service",
    audience: str = "service",
    session_id: str = get_id(),
) -> tuple[str, str]:
    now = int(time.time())

    access_payload = AccessTokenPayload(
        iss=issuer,
        aud=audience,
        sub=subject,
        sid=session_id,
        iat=now,
        exp=now + JWT_ACCESS_TOKEN_TTL,
        nbf=now,
        jti=get_id(),
    )

    refresh_payload = RefreshTokenPayload(
        sub=subject,
        sid=session_id,
        iat=now,
        exp=now + JWT_REFRESH_TOKEN_TTL,
        nbf=now,
        jti=get_id(),
    )

    access_token = encode(access_payload)
    refresh_token = encode(refresh_payload)

    return access_token, refresh_token
