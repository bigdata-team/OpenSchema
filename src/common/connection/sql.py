from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from common.config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    SERVICE_DB_SCHEMA,
)

from .connection import ConnectionBase


class SqlConnectionBase(ConnectionBase):
    def __init__(self, url: str, schema: str):
        self.url = url
        self.schema = schema
        self.engine = create_async_engine(url, pool_pre_ping=True)
        self.session_maker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_schema(self):
        async with self.engine.begin() as conn:
            await conn.exec_driver_sql(f"CREATE SCHEMA IF NOT EXISTS {self.schema};")
        await self.engine.dispose()

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        await self.engine.dispose()

    async def __aenter__(self):
        await self.create_schema()
        await self.create_tables()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.engine.dispose()

    async def unpack(self):
        async with self.session_maker() as session:
            yield session


class PostgresConnection(SqlConnectionBase):
    def __init__(
        self,
        host: str = POSTGRES_HOST,
        port: int = POSTGRES_PORT,
        user: str = POSTGRES_USER,
        password: str = POSTGRES_PASSWORD,
        db: str = POSTGRES_DB,
        schema: str = SERVICE_DB_SCHEMA,
    ):
        url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        super().__init__(url, schema)
