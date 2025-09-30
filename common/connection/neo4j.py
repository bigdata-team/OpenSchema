import os
from contextlib import asynccontextmanager, contextmanager

from neo4j import AsyncGraphDatabase, GraphDatabase

NEO4J_HOST = os.getenv("NEO4J_HOST")
NEO4J_PORT = int(os.getenv("NEO4J_PORT"))
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

NEO4J_URI = f"bolt://{NEO4J_HOST}:{NEO4J_PORT}"

async_engine = AsyncGraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
)

engine = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
)


@asynccontextmanager
async def get_aioneo4j():
    async with async_engine.session() as session:
        yield session


@contextmanager
def get_neo4j():
    with engine.session() as session:
        yield session
