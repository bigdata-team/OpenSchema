import os
from ._base import unpack, Connection, AsyncConnection, Registry
from common.util.hash import sha1


class RedisConnection(Connection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("REDIS_HOST"),
        port: str = os.getenv("REDIS_PORT"),
        password: str = os.getenv("REDIS_PASSWORD"),
        db: str = os.getenv("REDIS_DB"),
    ):
        import redis

        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.key = key or f"sync.redis.{self.host}.{self.port}.{self.password}.{self.db}"

        if not Registry.has(self.key):
            session = redis.from_url(self.uri)
            Registry.register(self.key, {"session": session})

        self.session: redis.Redis = Registry.get(self.key)["session"]

    @property
    def uri(self):
        if self.password is None:
            return f"redis://{self.host}:{self.port}/{self.db}"
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"

    def connect(self):
        return self.session.ping()


class AsyncRedisConnection(AsyncConnection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("REDIS_HOST"),
        port: str = os.getenv("REDIS_PORT"),
        password: str = os.getenv("REDIS_PASSWORD"),
        db: str = os.getenv("REDIS_DB"),
    ):
        import redis

        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.key = key or f"async.redis.{self.host}.{self.port}.{self.password}.{self.db}"

        if not Registry.has(self.key):
            session = redis.asyncio.from_url(self.uri)
            Registry.register(self.key, {"session": session})

        self.session: redis.asyncio.Redis = Registry.get(self.key)["session"]

    @property
    def uri(self):
        if self.password is None:
            return f"redis://{self.host}:{self.port}/{self.db}"
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"

    async def connect(self):
        return await self.session.ping()
