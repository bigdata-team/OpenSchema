import os

from common.util.hash import sha1

from ._base import AsyncConnection, Connection, Registry, unpack


class MongoConnection(Connection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("MONGO_HOST"),
        port: str = os.getenv("MONGO_PORT"),
        user: str = os.getenv("MONGO_USER"),
        password: str = os.getenv("MONGO_PASSWORD"),
        db: str = os.getenv("MONGO_DB"),
    ):
        from pymongo import MongoClient, database

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

        self.key = key or f"sync.mongo.{self.host}.{self.port}.{self.user}.{self.db}"

        if not Registry.has(self.key):
            client = MongoClient(self.uri)
            Registry.register(
                self.key,
                {
                    "client": client,
                },
            )

        self.client = Registry.get(self.key)["client"]
        self.session: database.Database = self.client[self.db]

    @property
    def uri(self):
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}"

    def connect(self):
        return self.session.command("ping")


class AsyncMongoConnection(AsyncConnection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("MONGO_HOST"),
        port: str = os.getenv("MONGO_PORT"),
        user: str = os.getenv("MONGO_USER"),
        password: str = os.getenv("MONGO_PASSWORD"),
        db: str = os.getenv("MONGO_DB"),
    ):
        from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

        self.key = key or f"async.mongo.{self.host}.{self.port}.{self.user}.{self.db}"

        if not Registry.has(self.key):
            client = AsyncIOMotorClient(self.uri)
            Registry.register(
                self.key,
                {
                    "client": client,
                },
            )

        self.client = Registry.get(self.key)["client"]
        self.session: AsyncIOMotorDatabase = self.client[self.db]

    @property
    def uri(self):
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}"

    async def connect(self):
        return await self.session.command("ping")
