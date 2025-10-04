import os
from ._base import unpack, Connection, AsyncConnection, Registry
from common.util.hash import sha1


class PostgresConnection(Connection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("POSTGRES_HOST"),
        port: str = os.getenv("POSTGRES_PORT"),
        user: str = os.getenv("POSTGRES_USER"),
        password: str = os.getenv("POSTGRES_PASSWORD"),
        db: str = os.getenv("POSTGRES_DB"),
    ):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker, Session

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.key = key or f"sync.postgres.{self.host}.{self.port}.{self.user}.{self.db}"

        if not Registry.has(self.key):
            engine = create_engine(self.uri, pool_pre_ping=True)
            session_maker = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
                expire_on_commit=False,
            )

            Registry.register(
                self.key,
                {
                    "engine": engine,
                    "session_maker": session_maker,
                },
            )

        self.engine = Registry.get(self.key)["engine"]
        self.session_maker = Registry.get(self.key)["session_maker"]

        self.session: Session = None

    @property
    def uri(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    def __enter__(self):
        self.session = self.session_maker()
        self.session.__enter__()
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        try:
            if exc_type:
                self.session.rollback()
        finally:
            if self.session:
                self.session.close()
            self.session = None

    @unpack
    def connect(self):
        from sqlalchemy import text

        return self.session.execute(text("SELECT 1"))


class AsyncPostgresConnection(AsyncConnection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("POSTGRES_HOST"),
        port: str = os.getenv("POSTGRES_PORT"),
        user: str = os.getenv("POSTGRES_USER"),
        password: str = os.getenv("POSTGRES_PASSWORD"),
        db: str = os.getenv("POSTGRES_DB"),
    ):
        from sqlalchemy.ext.asyncio import (
            AsyncSession,
            async_sessionmaker,
            create_async_engine,
        )

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.key = key or f"async.postgres.{self.host}.{self.port}.{self.user}.{self.db}"

        if not Registry.has(self.key):
            engine = create_async_engine(self.uri, pool_pre_ping=True)
            session_maker = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

            Registry.register(
                self.key,
                {
                    "engine": engine,
                    "session_maker": session_maker,
                },
            )

        self.engine = Registry.get(self.key)["engine"]
        self.session_maker = Registry.get(self.key)["session_maker"]

        self.session: AsyncSession = None

    @property
    def uri(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    async def __aenter__(self):
        self.session = self.session_maker()
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        try:
            if exc_type:
                await self.session.rollback()
        finally:
            if self.session:
                await self.session.close()
            self.session = None

    @unpack
    async def connect(self):
        from sqlalchemy import text

        return await self.session.execute(text("SELECT 1"))
