from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from neo4j import AsyncGraphDatabase

from common.config.const import (
    NEO4J_DB,
    NEO4J_HOST,
    NEO4J_PASSWORD,
    NEO4J_PORT,
    NEO4J_USER,
)


def create_neo4j_lifespan(
    key: str = "neo4j",
    host: str = NEO4J_HOST,
    port: str = NEO4J_PORT,
    user: str = NEO4J_USER,
    password: str = NEO4J_PASSWORD,
    db: str = NEO4J_DB,
):

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "connection"):
            app.state.connection = {}

        uri = f"bolt://{host}:{port}"
        driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

        app.state.connection[key] = {
            "driver": driver,
            "db": db,
        }
        try:
            yield
        finally:
            await driver.close()

    return lifespan


def get_neo4j_session(key: str = "neo4j"):
    async def _unpack(request: Request):
        resource = request.app.state.connection[key]
        async with resource.get("driver").session(
            database=resource.get("db")
        ) as session:
            yield session

    return _unpack
