from datetime import datetime
from typing import Type, TypeVar

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import BaseModel

from common.config.const import SERVICE_DB_SCHEMA
from common.lifespan import get_crid
from common.lifespan.kafka import get_kafka_session
from common.lifespan.mongo import get_mongo_session
from common.repository.kafka import KafkaMixin

from .repository import Repository

T = TypeVar("T", bound=BaseModel)


class MongoRepository(Repository[T]):
    def __init__(self, model: Type[T], mongo: AsyncIOMotorDatabase):
        super().__init__(model)
        self.mongo: AsyncIOMotorDatabase = mongo

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.mongo[f"{SERVICE_DB_SCHEMA}.{self.model.__name__.lower()}"]

    async def connect(self) -> None:
        await self.mongo.list_collection_names()

    async def create(self, obj: T) -> T:
        await self.collection.insert_one(obj.model_dump())
        return obj

    async def get(self, id: str) -> T | None:
        result = await self.collection.find_one(
            {"id": id, "deleted_at": None}, projection={"_id": False}
        )
        return result

    async def update(self, id: str, obj: T) -> T | None:
        result = await self.collection.find_one_and_update(
            {"id": id, "deleted_at": None},
            {"$set": obj.model_dump(exclude={"id", "created_at", "delted_at"})},
            projection={"_id": False},
            return_document=True,
        )
        return result

    async def delete(self, id: str) -> T | None:
        result = await self.collection.find_one_and_update(
            {"id": id, "deleted_at": None},
            {"$set": {"deleted_at": datetime.now()}},
            projection={"_id": False},
            return_document=True,
        )
        return result


class KafkaMongoRepository(MongoRepository[T], KafkaMixin):
    def __init__(self, model: Type[T], mongo: AsyncIOMotorDatabase, kafka, crid: str):
        MongoRepository.__init__(self, model=model, mongo=mongo)
        KafkaMixin.__init__(self, model=model, kafka=kafka, crid=crid)

    async def connect(self) -> None:
        await MongoRepository.connect(self)
        await self.publish_event(payload={"event": "connected"}, action="connected")

    async def create(self, obj: T) -> T:
        obj = await MongoRepository.create(self, obj)
        print(await self.publish_event(payload=obj.model_dump(), action="created"))
        return obj

    async def get(self, id: str) -> T | None:
        obj = await MongoRepository.get(self, id)
        if obj:
            await self.publish_event(payload=obj.model_dump(), action="retrieved")
        return obj

    async def update(self, id: str, obj: T) -> T | None:
        obj = await MongoRepository.update(self, id, obj)
        if obj:
            await self.publish_event(payload=obj.model_dump(), action="updated")
        return obj

    async def delete(self, id: str) -> T | None:
        obj = await MongoRepository.delete(self, id)
        if obj:
            await self.publish_event(payload=obj.model_dump(), action="deleted")
        return obj


def create_mongo_repo(model: Type[T]) -> callable:
    def _get_repo(
        mongo=Depends(get_mongo_session()),
    ) -> MongoRepository[T]:
        return MongoRepository(model=model, mongo=mongo)

    return _get_repo


def create_kafka_mongo_repo(model: Type[T]) -> callable:
    def _get_repo(
        mongo=Depends(get_mongo_session()),
        kafka=Depends(get_kafka_session()),
        crid=Depends(get_crid()),
    ) -> KafkaMongoRepository[T]:
        return KafkaMongoRepository(model=model, mongo=mongo, kafka=kafka, crid=crid)

    return _get_repo
