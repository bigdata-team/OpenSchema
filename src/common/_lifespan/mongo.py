from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from common.config import MONGO_DB, MONGO_HOST, MONGO_PASSWORD, MONGO_PORT, MONGO_USER
from common.model.mongo import DocumentRegistry


def create_mongo_lifespan(
    key: str = "mongo",
    host: str = MONGO_HOST,
    port: str = MONGO_PORT,
    user: str = MONGO_USER,
    password: str = MONGO_PASSWORD,
    db: str = MONGO_DB,
):
    url = f"mongodb://{user}:{password}@{host}:{port}"

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "connection"):
            app.state.connection = {}

        client = AsyncIOMotorClient(url)
        session: AsyncIOMotorDatabase = client[db]

        await init_beanie(
            database=session, document_models=[*DocumentRegistry.retrieve()]
        )

        app.state.connection[key] = {
            "session": session,
        }
        yield
        await client.close()

    return lifespan


def get_mongo_session(key: str = "mongo"):
    async def _unpack(request: Request) -> AsyncIOMotorClient:
        resource = request.app.state.connection[key]
        return resource.get("session")

    return _unpack
