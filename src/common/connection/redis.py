from common.config import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_USER

from .connection import ConnectionBase


class RedisConnectionBase(ConnectionBase):
    def __init__(self, host: str, port: int, user: str, password: str, db: int):
        import redis

        self.url = f"redis://{user}:{password}@{host}:{port}/{db}"
        self.session = redis.asyncio.from_url(self.url)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def unpack(self):
        return self.session


class RedisConnection(RedisConnectionBase):
    def __init__(
        self,
        host: str = REDIS_HOST,
        port: int = REDIS_PORT,
        user: str = REDIS_USER,
        password: str = REDIS_PASSWORD,
        db: int = REDIS_DB,
    ):
        super().__init__(host, port, user, password, db)
