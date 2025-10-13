from typing import Type, TypeVar

import redis as r
from fastapi import Depends
from pydantic import BaseModel
from redis.asyncio import Redis

from common.config.const import SERVICE_DB_SCHEMA
from common.lifespan.redis import get_redis_session

from .repository import Repository

T = TypeVar("T", bound=BaseModel | str)


class RedisRepository(Repository[T]):
    def __init__(self, model: Type[T], redis: Redis):
        super().__init__(model)
        self.redis: Redis = redis

    async def connect(self) -> None:
        await self.redis.ping()

    async def create_or_update(self, id: str, obj: T, ttl: int = 60) -> T:
        key = f"{SERVICE_DB_SCHEMA}:{id}"
        tmp = obj
        if not isinstance(tmp, str):
            tmp = tmp.model_dump_json()
        await self.redis.set(key, tmp, ex=ttl)
        return obj

    async def get(self, id: str) -> T | None:
        key = f"{SERVICE_DB_SCHEMA}:{id}"
        value = await self.redis.get(key)
        if value:
            if self.model is str:
                return value.decode()
            return self.model.model_validate_json(value)
        return None

    async def delete(self, id: str) -> T | None:
        key = f"{SERVICE_DB_SCHEMA}:{id}"
        value = await self.redis.get(key)
        if value:
            await self.redis.delete(key)
            if self.model is str:
                return value.decode()
            return self.model.model_validate_json(value)
        return None


def create_redis_repo(model: Type[T]) -> callable:
    async def _get_repo(
        redis=Depends(get_redis_session()),
    ) -> RedisRepository[T]:
        return RedisRepository(model, redis)

    return _get_repo
