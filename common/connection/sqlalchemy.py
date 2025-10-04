import os
from ._base import unpack, Connection, AsyncConnection, Registry


class SQLConnection(Connection):
    def __init__(self, uri: str, key: str = None):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker, Session

        self.key = key or f"sync.sql.{uri}"
        self.uri = uri

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


class AsyncSQLConnection(AsyncConnection):
    def __init__(self, uri: str, key: str = None):
        from sqlalchemy.ext.asyncio import (
            AsyncSession,
            async_sessionmaker,
            create_async_engine,
        )

        self.uri = uri
        self.key = key or f"async.sql.{uri}"

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
