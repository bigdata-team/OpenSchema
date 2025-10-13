from datetime import datetime
from typing import Type, TypeVar

from aiokafka import AIOKafkaProducer
from common.connection import get_session
from common.connection.kafka import KafkaSession
from common.connection.mongo import MongoSession
from common.const import SERVICE_DB_SCHEMA
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import BaseModel

from .kafka import KafkaRepository, KafkaTopicMixin
from .repository import Repository

T = TypeVar("T", bound=BaseModel)


class MongoRepository(Repository[T]):
    def __init__(
        self,
        model: Type[T],
        session: AsyncIOMotorDatabase,
    ):
        super().__init__(model, session)

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.session[f"{SERVICE_DB_SCHEMA}_{self.model.__name__.lower()}"]

    async def connect(self, crid: str | None = None) -> None:
        await self.session.list_collection_names()

    async def create(self, obj: T, crid: str | None = None) -> T:
        await self.collection.insert_one(obj.model_dump())
        return obj

    async def get(self, id: str, crid: str | None = None) -> T | None:
        result = await self.collection.find_one(
            {"id": id, "deleted_at": None}, projection={"_id": False}
        )
        return result

    async def update(self, id: str, obj: T, crid: str | None = None) -> T | None:
        result = await self.collection.find_one_and_update(
            {"id": id, "deleted_at": None},
            {"$set": obj.model_dump(exclude={"id", "created_at", "delted_at"})},
            projection={"_id": False},
            return_document=True,
        )
        return result

    async def delete(self, id: str, crid: str | None = None) -> T | None:
        result = await self.collection.find_one_and_update(
            {"id": id, "deleted_at": None},
            {"$set": {"deleted_at": datetime.now()}},
            projection={"_id": False},
            return_document=True,
        )
        return result


class KafkaMongoRepository(MongoRepository[T], KafkaTopicMixin):
    def __init__(
        self,
        model: Type[T],
        session: AsyncIOMotorDatabase,
        kafka_session: AIOKafkaProducer,
    ):
        super().__init__(model, session)
        self.kafka = KafkaRepository(kafka_session)

    async def create(self, obj: T, crid: str | None = None) -> T:
        obj = await super().create(obj, crid)
        topic = self.create_kafka_topic("created")
        await self.kafka.create_event(topic=topic, payload=obj, crid=crid)
        return obj

    async def get(self, id: str, crid: str | None = None) -> T | None:
        obj = await super().get(id, crid)
        if obj:
            topic = self.create_kafka_topic("retrieved")
            await self.kafka.create_event(topic=topic, payload=obj, crid=crid)
        return obj

    async def update(self, id: str, obj: T, crid: str | None = None) -> T | None:
        obj = await super().update(id, obj, crid)
        if obj:
            topic = self.create_kafka_topic("updated")
            await self.kafka.create_event(topic=topic, payload=obj, crid=crid)
        return obj

    async def delete(self, id: str, crid: str | None = None) -> T | None:
        obj = await super().delete(id, crid)
        if obj:
            topic = self.create_kafka_topic("deleted")
            await self.kafka.create_event(topic=topic, payload=obj, crid=crid)
        return obj
