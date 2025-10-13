from typing import Type, TypeVar

import redis
from common.connection import get_session
from common.connection.redis import RedisSession
from common.const import SERVICE_DB_SCHEMA
from fastapi import Depends
from pydantic import BaseModel

from .repository import Repository

T = TypeVar("T", bound=BaseModel | str)


class RedisRepository(Repository[T]):
    def __init__(self, model: Type[T], session: redis.asyncio.Redis):
        super().__init__(model, session)
        self.session: redis.asyncio.Redis

    async def connect(self, crid: str | None = None) -> None:
        await self.session.ping()

    async def create_or_update(
        self, id: str, model: T, ttl: int = 60, crid: str | None = None
    ) -> T:
        key = f"{SERVICE_DB_SCHEMA}:{id}"
        if not isinstance(model, str):
            model = model.model_dump_json()
        await self.session.set(key, model, ex=ttl)
        return model

    async def get(self, id: str, crid: str | None = None) -> str | None:
        key = f"{SERVICE_DB_SCHEMA}:{id}"
        value = await self.session.get(key)
        if value:
            if self.model is str:
                return value.decode()
            return self.model.model_validate_json(value)
        return None

    async def delete(self, id: str, crid: str | None = None) -> str | None:
        key = f"{SERVICE_DB_SCHEMA}:{id}"
        value = await self.session.get(key)
        if value:
            await self.session.delete(key)
            if self.model is str:
                return value.decode()
            return self.model.model_validate_json(value)
        return None


def get_redis_repodep(model: Type[T]) -> callable:
    async def _get_repo(
        session: redis.asyncio.Redis = Depends(get_session(RedisSession)),
    ) -> RedisRepository[T]:
        return RedisRepository(model, session)

    return _get_repo
