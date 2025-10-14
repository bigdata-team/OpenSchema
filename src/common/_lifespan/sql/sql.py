from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from common.config import SERVICE_DB_SCHEMA


async def _create_schema(engine, schema):
    async with engine.begin() as conn:
        await conn.exec_driver_sql(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    await engine.dispose()


async def _create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await engine.dispose()


def create_sql_lifespan(key: str, url: str):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "connection"):
            app.state.connection = {}

        engine = create_async_engine(url, pool_pre_ping=True)
        session_maker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        await _create_schema(engine, SERVICE_DB_SCHEMA)
        await _create_tables(engine)

        app.state.connection[key] = {
            "session_maker": session_maker,
        }
        try:
            yield
        finally:
            await engine.dispose()

    return lifespan


def get_sql_session(key: str):
    async def _unpack(request: Request):
        resource = request.app.state.connection[key]
        async with resource.get("session_maker")() as session:
            yield session

    return _unpack
