from common.config import MONGO_DB, MONGO_HOST, MONGO_PASSWORD, MONGO_PORT, MONGO_USER
from common.model.mongo import DocumentRegistry

from .connection import ConnectionBase


class MongoConnectionBase(ConnectionBase):
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        db: str,
    ):
        from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

        self.url = f"mongodb://{user}:{password}@{host}:{port}"
        self.db_name = db
        self.client = AsyncIOMotorClient(self.url)
        self.session: AsyncIOMotorDatabase = self.client[db]

    async def __aenter__(self):
        from beanie import init_beanie

        await init_beanie(
            database=self.session, document_models=[*DocumentRegistry.retrieve()]
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()

    async def unpack(self):
        return self.session


class MongoConnection(MongoConnectionBase):
    def __init__(
        self,
        host: str = MONGO_HOST,
        port: int = MONGO_PORT,
        user: str = MONGO_USER,
        password: str = MONGO_PASSWORD,
        db: str = MONGO_DB,
    ):
        super().__init__(host, port, user, password, db)
