import inspect
from abc import ABC

from sqlalchemy import text

from common.connection.kafka import get_aiokafka_producer
from common.connection.mongo import get_aiomongo
from common.connection.neo4j import get_aioneo4j, get_neo4j
from common.connection.postgres import get_aiopostgres, get_postgres
from common.connection.redis import get_aioredis, get_redis
from common.connection.s3 import get_aios3, get_s3
from common.util import now


def context(method):
    async def _wrapped(self, *args, **kwargs):
        conn = self.connection()

        if hasattr(conn, "__aenter__") and hasattr(conn, "__aexit__"):
            session = await conn.__aenter__()
            self.session = session
            try:
                return await method(self, *args, **kwargs)
            finally:
                self.session = None
                await conn.__aexit__(None, None, None)

        elif hasattr(conn, "__enter__") and hasattr(conn, "__exit__"):
            session = conn.__enter__()
            self.session = session
            try:
                return method(self, *args, **kwargs)
            finally:
                self.session = None
                conn.__exit__(None, None, None)

        elif inspect.isawaitable(conn):
            self.session = await conn
            try:
                return await method(self, *args, **kwargs)
            finally:
                self.session = None
        else:
            self.session = conn
            try:
                return method(self, *args, **kwargs)
            finally:
                self.session = None

    return _wrapped


class Repository(ABC):
    def __init__(
        self,
        name: str = None,
        connection: callable = None,
    ):
        self.name = name or self.__class__.__name__
        self.connection = connection
        self.session = None

    @context
    def connect(self):
        raise NotImplementedError


class AsyncRepository(ABC):
    def __init__(
        self,
        name: str = None,
        connection: callable = None,
    ):
        self.name = name or self.__class__.__name__
        self.connection = connection
        self.session = None

    @context
    async def connect(self):
        raise NotImplementedError


class PostgresRepository(Repository):
    def __init__(self, name="postgres", connection=get_postgres):
        super().__init__(name, connection)
        from sqlalchemy.orm import Session

        self.session: Session

    @context
    def connect(self):
        self.session.execute(text("SELECT 1"))


class AsyncPostgresRepository(AsyncRepository):
    def __init__(self, name="aiopostgres", connection=get_aiopostgres):
        super().__init__(name, connection)
        from sqlalchemy.ext.asyncio import AsyncSession

        self.session: AsyncSession

    @context
    async def connect(self):
        await self.session.execute(text("SELECT 1"))


class AsyncMongoRepository(AsyncRepository):
    def __init__(self, name="aiomongo", connection=get_aiomongo):
        super().__init__(name, connection)
        from motor.motor_asyncio import AsyncIOMotorDatabase

        self.session: AsyncIOMotorDatabase

    @context
    async def connect(self):
        await self.session.command("ping")


class Neo4jRepository(Repository):
    def __init__(self, name="neo4j", connection=get_neo4j):
        super().__init__(name, connection)
        from neo4j import Session

        self.session: Session

    @context
    def connect(self):
        self.session.run("RETURN 1")


class AsyncNeo4jRepository(AsyncRepository):
    def __init__(self, name="aioneo4j", connection=get_aioneo4j):
        super().__init__(name, connection)
        from neo4j import AsyncSession

        self.session: AsyncSession

    @context
    async def connect(self):
        await self.session.run("RETURN 1")


class S3Repository(Repository):
    def __init__(self, name="s3", connection=get_s3):
        super().__init__(name, connection)
        from boto3 import Session

        self.session: Session

    @context
    def connect(self):
        self.session.list_buckets()


class AsyncS3Repositry(AsyncRepository):
    def __init__(self, name="aios3", connection=get_aios3):
        super().__init__(name, connection)
        from aioboto3 import Session

        self.session: Session

    @context
    async def connect(self):
        await self.session.list_buckets()


class RedisRepository(Repository):
    def __init__(self, name="redis", connection=get_redis):
        super().__init__(name, connection)
        from redis import Redis

        self.session: Redis

    @context
    def connect(self):
        self.session.ping()


class AsyncRedisRepository(AsyncRepository):
    def __init__(self, name="aioredis", connection=get_aioredis):
        super().__init__(name, connection)
        from redis.asyncio import Redis

        self.session: Redis

    @context
    async def connect(self):
        await self.session.ping()


class AsyncKafkaRepository(AsyncRepository):
    def __init__(self, name="aiokafka_produer", connection=get_aiokafka_producer):
        super().__init__(name, connection)
        from aiokafka import AIOKafkaProducer

        self.session: AIOKafkaProducer

    @context
    async def connect(self):
        ts = now().isoformat()
        await self.session.send_and_wait("connect", f"[connect] {ts}".encode())
