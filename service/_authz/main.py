import os
import random

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from models.db import *
from models.http import *
from sqlalchemy import text

from common.jwt import get_tokens
from common.lifespan import compose, kafka, postgres, redis
from common.middleware import CorrelationIdMiddleware
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response
from common.connection.util.util import get_random_name, hash_password, verify_password

app = FastAPI(
    root_path="/api/v1/auth",
    lifespan=compose(kafka, postgres, redis),
)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz(request: Request):
    async with app.state.postgres_session() as session:
        await session.execute(text("SELECT 1"))
    await app.state.redis.ping()
    return create_response("Ok", "Authorization service is healthy.", None, 200)


@app.post("/register", response_model=TokensModel)
async def register(request: Request, body: AuthCredentialsModel):
    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        result = await db.execute(select(User).where(User.email == body.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            return create_response("Conflict", "Email already exists.", None, 409)

        while True:
            username = get_random_name() + "_" + str(random.randint(1000, 9999))
            result = await db.execute(select(User).where(User.username == username))
            if result.scalar_one_or_none() is None:
                break

        hashed_password = hash_password(body.password)
        user = User(
            email=body.email,
            username=username,
            hashed_password=hashed_password,
            is_active=True,
            is_first_login=True,
            change_password_on_next_login=False,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

    try:
        await app.state.kafka_producer.send_and_wait(
            "auth.user.registered",
            key=None,
            value=create_event(payload=user.to_dict(), cid=request.state.cid),
        )

    except Exception as e:
        return create_response("Kafka event error", str(e), 500)

    return create_response("Created", "User registered.", None, 201)


@app.post("/login", response_model=DataResponseModel[TokensModel])
async def login(request: Request, body: AuthCredentialsModel):
    from sqlalchemy.future import select

    async with app.state.postgres_session() as db:
        result = await db.execute(select(User).where(User.email == body.email))
        user = result.scalar_one_or_none()
        if user and verify_password(body.password, user.hashed_password):
            from datetime import datetime, timezone

            user.last_login_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(user)
        else:
            return create_response(
                "Unauthorized", "Invalid email or password.", None, 401
            )

    tokens = jwt.claim_tokens(sub=user.id)

    res = create_response("Ok", "Logged in successfully.", tokens, 200)

    res.set_cookie(
        key="access_token",
        value=tokens.get("access_token"),
        httponly=True,
        secure=True,
        samesite="None",
        max_age=jwt.access_token_ttl,
        path="/",
    )

    res.set_cookie(
        key="refresh_token",
        value=tokens.get("refresh_token"),
        httponly=True,
        secure=True,
        samesite="None",
        max_age=jwt.refresh_token_ttl,
        path="/api/v1/auth/refresh",
    )

    return res


@app.post("/logout", response_model=AccessTokenModel)
async def logout(request: Request, tokens=Depends(get_tokens)):
    token = tokens.get("access_token") or tokens.get("bearer_token") or None
    payload = await jwt.verify_token(token, "auth.service", "service")
    jwt.blacklist(payload.sub)
    res = create_response("Ok", "Logged out successfully.", None, 200)
    res.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        # TODO: https
        secure=True,
        samesite="None",
        max_age=0,
        path="/",
    )

    res.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        # TODO: https
        secure=True,
        samesite="None",
        max_age=0,
        path="/api/v1/auth/refresh",
    )
    return res


@app.post("/refresh", response_model=AccessTokenModel)
async def refresh(request: Request, tokens=Depends(get_tokens)):
    token = tokens.get("refresh_token") or tokens.get("bearer_token") or None
    refreshed_tokens = await jwt.rotate_tokens(
        refresh_token=token, iss="auth.service", aud="service"
    )

    res = create_response("Ok", "Refreshed tokens successfully.", refreshed_tokens, 200)

    res.set_cookie(
        key="access_token",
        value=refreshed_tokens.get("access_token"),
        httponly=True,
        # TODO: https
        secure=True,
        samesite="None",
        max_age=jwt.access_token_ttl,
        path="/",
    )

    res.set_cookie(
        key="refresh_token",
        value=refreshed_tokens.get("refresh_token"),
        httponly=True,
        # TODO: https
        secure=True,
        samesite="None",
        max_age=jwt.refresh_token_ttl,
        path="/api/v1/auth/refresh",
    )

    return res


@app.get("/me", response_model=DataResponseModel[MeModel])
async def get_me(tokens: dict = Depends(get_tokens)):
    token = tokens.get("access_token") or tokens.get("bearer_token") or None
    payload = await jwt.verify_token(token, issuer="auth.service", audience="service")

    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        result = await db.execute(select(User).where(User.id == payload.sub))
        user = result.scalar_one_or_none()

    if not user:
        return create_response("User not found.", None, None, 404)

    return create_response(
        "Ok",
        "User retrieved successfully.",
        MeModel(
            email=user.email,
            username=user.username,
            name=user.name,
            bio=user.bio,
            profile_url=user.profile_url,
            role=user.role,
            is_first_login=user.is_first_login,
            is_active=user.is_active,
            change_password_on_next_login=user.change_password_on_next_login,
        ).model_dump(),
        200,
    )


@app.post("/me/change-password")
async def change_password(
    body: ChangePasswordModel,
    tokens: dict = Depends(get_tokens),
):
    token = tokens.get("access_token") or tokens.get("bearer_token") or None
    payload = await jwt.verify_token(token, issuer="auth.service", audience="service")

    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        result = await db.execute(select(User).where(User.id == payload.sub))
        user = result.scalar_one_or_none()
        if not user or not verify_password(body.old_password, user.hashed_password):
            return create_response(
                "Not found", "User not found or old password incorrect.", None, 404
            )

        user.hashed_password = hash_password(body.new_password)
        await db.commit()
        await db.refresh(user)

    return create_response("Ok", "Password changed successfully.", None, 200)
