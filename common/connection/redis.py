import os
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

async def get_redis():
    return await redis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        password=REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
    )