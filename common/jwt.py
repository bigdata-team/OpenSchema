import os
import uuid
from datetime import datetime, timedelta, timezone

from redis.asyncio import Redis
from fastapi import HTTPException
from jose import jwt
from pydantic import BaseModel
from .connection.redis import get_redis
from fastapi import Request
from fastapi import Header, Request

# JWT_SECRET=supersecret!
# JWT_ALGORITHM=HS256
# JWT_ACCESS_TOKEN_EXPIRE_SECONDS=60
# JWT_REFRESH_TOKEN_EXPIRE_SECONDS=180


class TokenPayload(BaseModel):
    sid: str
    sub: str
    iat: int
    exp: int
    jti: str


class AccessTokenPayload(TokenPayload):
    iss: str
    aud: str


class RefreshTokenPayload(TokenPayload):
    pass


class JWTService:
    def __init__(
        self,
        secret: str = os.getenv("JWT_SECRET", "supersecret!"),
        algorithm: str = os.getenv("JWT_ALGORITHM", "HS256"),
    ):
        self.secret = secret
        self.algorithm = algorithm

    def decode(
        self, token: str, issuer: str | None = None, audience: str | None = None
    ) -> dict:
        return jwt.decode(
            token,
            self.secret,
            algorithms=[self.algorithm],
            issuer=issuer,
            audience=audience,
        )

    def verify_token(
        self, token: str, issuer: str | None = None, audience: str | None = None
    ) -> TokenPayload:
        try:
            payload = TokenPayload(
                **self.decode(token, issuer=issuer, audience=audience)
            )
        except:
            raise HTTPException(status_code=401, detail="Token is invalid.")

        if payload.exp < int(datetime.now(timezone.utc).timestamp()):
            raise HTTPException(status_code=401, detail="Token has expired.")

        return payload


class JWTManager(JWTService):
    def __init__(
        self,
        secret: str = os.getenv("JWT_SECRET", "supersecret!"),
        algorithm: str = os.getenv("JWT_ALGORITHM", "HS256"),
        access_token_ttl: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_SECONDS", 60)
        ),
        refresh_token_ttl: int = int(
            os.getenv("JWT_REFRESH_TOKEN_EXPIRE_SECONDS", 180)
        ),
    ):
        super().__init__(secret, algorithm)
        self.access_token_ttl = access_token_ttl
        self.refresh_token_ttl = refresh_token_ttl

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode(self, *args, **kwargs) -> dict:
        return super().decode(*args, **kwargs)

    def claim_tokens(
        self,
        sub: str,
        sid: str = None,
        iss: str = "auth.service",
        aud: str = "service",
    ) -> dict:
        if sid is None:
            sid = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        access_token_payload = AccessTokenPayload(
            sid=sid,
            iss=iss,
            aud=aud,
            sub=sub,
            iat=int(now.timestamp()),
            exp=int(
                (now + timedelta(seconds=self.access_token_ttl)).timestamp()
            ),
            jti=str(uuid.uuid4()),
        )

        refresh_token_payload = RefreshTokenPayload(
            sid=sid,
            sub=sub,
            iat=int(now.timestamp()),
            exp=int(
                (now + timedelta(seconds=self.refresh_token_ttl)).timestamp()
            ),
            jti=str(uuid.uuid4()),
        )

        return {
            "access_token": self.encode(access_token_payload.model_dump()),
            "refresh_token": self.encode(refresh_token_payload.model_dump()),
        }

    async def verify_token(
        self,
        token: str,
        issuer: str | None = None,
        audience: str | None = None,
    ) -> TokenPayload:
        import logging

        logger = logging.getLogger("jwt")
        try:
            payload: TokenPayload = super().verify_token(
                token, issuer=issuer, audience=audience
            )
            logger.debug(f"Decoded token payload: {payload}")
        except Exception as e:
            logger.error(f"Token decode/validation failed: {e}")
            raise e

        redis = await get_redis()
        sid_blacklisted = await redis.exists(f"bl:{payload.sid}")
        jti_blacklisted = await redis.exists(f"bl:{payload.jti}")
        logger.debug(
            f"sid_blacklisted={sid_blacklisted}, jti_blacklisted={jti_blacklisted}"
        )
        logger.debug(
            f"exp={payload.exp}, now={int(datetime.now(timezone.utc).timestamp())}"
        )
        if sid_blacklisted:
            logger.warning(f"Token sid {payload.sid} is blacklisted.")
            raise HTTPException(status_code=401, detail="Token is blacklisted.")

        if jti_blacklisted:
            logger.warning(f"Token jti {payload.jti} is blacklisted.")
            raise HTTPException(status_code=401, detail="Token is blacklisted.")

        return payload

    async def blacklist(self, id: str) -> None:
        redis = await get_redis()
        await redis.setex(f"bl:{id}", self.refresh_token_ttl, "blacklisted")

    async def rotate_tokens(
        self,
        refresh_token: str,
        iss: str = "auth.service",
        aud: str = "service",
    ) -> dict:
        import logging

        logger = logging.getLogger("jwt")
        logger.info(f"Rotating tokens for refresh_token: {refresh_token}")
        try:
            payload: TokenPayload = await self.verify_token(refresh_token)
        except Exception as e:
            logger.error(f"Token rotation failed: {e}")
            raise
        await self.blacklist(payload.jti)
        logger.info(
            f"Rotated tokens for user: {payload.sub}, sid: {payload.sid}"
        )
        return self.claim_tokens(
            sub=payload.sub, sid=payload.sid, iss=iss, aud=aud
        )


def get_tokens(request: Request, authorization: str = Header(None)) -> str:
    access_token = request.cookies.get("access_token", None)
    refresh_token = request.cookies.get("refresh_token", None)
    bearer_token = (
        authorization.removeprefix("Bearer ")
        if authorization and authorization.startswith("Bearer ")
        else None
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "bearer_token": bearer_token,
    }
