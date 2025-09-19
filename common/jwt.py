import os
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Header, HTTPException, Request
from jose import jwt
from pydantic import BaseModel
from redis.asyncio import Redis

from .connection.redis import get_redis

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_SECONDS", 60))
JWT_REFRESH_TOKEN_EXPIRE_SECONDS = int(
    os.getenv("JWT_REFRESH_TOKEN_EXPIRE_SECONDS", 180)
)


class TokenPayload(BaseModel):
    sub: str
    sid: str
    iat: int
    exp: int
    jti: str


class AccessTokenPayload(TokenPayload):
    iss: str
    aud: str


class RefreshTokenPayload(TokenPayload):
    pass


def claim_tokens(
    sub: str,
    sid: str = None,
    iss: str = "auth.service",
    aud: str = "service",
) -> dict:
    if sid is None:
        sid = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    access_token_payload = AccessTokenPayload(
        sub=sub,
        sid=sid,
        iss=iss,
        aud=aud,
        iat=int(now.timestamp()),
        exp=int((now + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRE_SECONDS)).timestamp()),
        jti=str(uuid.uuid4()),
    )

    refresh_token_payload = RefreshTokenPayload(
        sub=sub,
        sid=sid,
        iat=int(now.timestamp()),
        exp=int(
            (now + timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRE_SECONDS)).timestamp()
        ),
        jti=str(uuid.uuid4()),
    )

    return {
        "access_token": encode(access_token_payload.model_dump()),
        "refresh_token": encode(refresh_token_payload.model_dump()),
    }


def encode(payload: dict) -> str:
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode(token: str, issuer: str = None, audience: str = None) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
        issuer=issuer,
        audience=audience,
    )


def verify_token(
    token: str, issuer: str = "auth.service", audience: str = "service"
) -> TokenPayload:
    try:
        payload = TokenPayload(**decode(token, issuer=issuer, audience=audience))
    except:
        raise HTTPException(status_code=401, detail="Token is invalid.")

    if payload.exp < int(datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=401, detail="Token has expired.")

    return payload


async def verify_token_now(*args, **kwargs) -> TokenPayload:
    payload = verify_token(*args, **kwargs)
    redis = await get_redis()
    sid_blacklisted = await redis.exists(f"bl:{payload.sid}")
    jti_blacklisted = await redis.exists(f"bl:{payload.jti}")
    if sid_blacklisted:
        raise HTTPException(status_code=401, detail="Token is blacklisted.")

    if jti_blacklisted:
        raise HTTPException(status_code=401, detail="Token is blacklisted.")

    return payload


def verify_access_token(*args, **kwargs):
    return verify_token(*args, **kwargs)


def verify_refresh_token(token):
    return verify_token(token=token, issuer=None, audience=None)


async def verify_access_token_now(*args, **kwargs):
    return await verify_token_now(*args, **kwargs)


async def verify_refresh_token_now(token):
    return await verify_token_now(token=token, issuer=None, audience=None)


async def blacklist(id: str) -> None:
    redis = await get_redis()
    await redis.setex(f"bl:{id}", JWT_REFRESH_TOKEN_EXPIRE_SECONDS, "blacklisted")


async def rotate_tokens(
    refresh_token: str,
    issuer: str = "auth.service",
    audience: str = "service",
) -> dict:
    payload = await verify_refresh_token_now(refresh_token)
    await blacklist(payload.jti)
    return claim_tokens(sub=payload.sub, sid=payload.sid, iss=issuer, aud=audience)


def get_tokens(request: Request, authorization: str = Header("Authorization")) -> str:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    bearer_token = request.headers.get("Authorization")
    if bearer_token:
        bearer_token = bearer_token.removeprefix("Bearer ")

    return {
        "cookie_access_token": access_token,
        "cookie_refresh_token": refresh_token,
        "bearer_token": bearer_token,
    }
