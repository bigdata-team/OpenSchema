import os

import redis.asyncio as redis
from redis import Redis

REDIS_DB = os.getenv("REDIS_DB")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


async def get_aioredis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD
):
    uri = f"redis://:{password}@{host}:{port}/{db}"
    return await redis.from_url(
        uri,
        password=REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
    )


def get_redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD):
    uri = f"redis://:{password}@{host}:{port}/{db}"
    return Redis.from_url(uri)
