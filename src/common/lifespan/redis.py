from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI, Request

from common.config import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USER


def create_redis_lifespan(
    key: str = "redis",
    host: str = REDIS_HOST,
    port: str = REDIS_PORT,
    user: str = REDIS_USER,
    password: str = REDIS_PASSWORD,
    db: str = REDIS_DB,
):
    url = f"redis://{user}:{password}@{host}:{port}/{db}"

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "connection"):
            app.state.connection = {}

        session: redis.asyncio.Redis = redis.asyncio.from_url(url)

        app.state.connection[key] = {
            "session": session,
        }
        try:
            yield
        finally:
            await session.close()

    return lifespan


def get_redis_session(key: str = "redis"):
    async def _unpack(request: Request) -> redis.asyncio.Redis:
        resource = request.app.state.connection[key]
        return resource.get("session")

    return _unpack
