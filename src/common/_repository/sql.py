from datetime import datetime
from typing import Type, TypeVar

from aiokafka import AIOKafkaProducer
from common.connection import get_session
from common.connection.kafka import KafkaSession
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, text

from common.model.sql import Base

from .kafka import KafkaRepository, KafkaTopicMixin
from .repository import Repository

T = TypeVar("T", bound=Base)


class SqlRepository(Repository[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        super().__init__(model, session)

    async def connect(self, crid: str | None = None) -> None:
        (await self.session.execute(text("SELECT 1"))).scalar_one()

    async def create(self, obj: T, crid: str | None = None) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, id: str, crid: str | None = None) -> T | None:
        query = select(self.model).where(
            self.model.id == id, self.model.deleted_at == None
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, id: str, obj: T, crid: str | None = None) -> T | None:
        prev_obj = await self.get(id)
        if not prev_obj:
            return None
        for key, value in obj.model_dump(
            exclude_unset=True,
            exclude={"id", "seq", "created_at", "updated_at", "deleted_at"},
        ).items():
            setattr(prev_obj, key, value)
        await self.session.commit()
        await self.session.refresh(prev_obj)
        return prev_obj

    async def delete(self, id: str, crid: str | None = None) -> T | None:
        obj = await self.get(id)
        if not obj:
            return None
        obj.deleted_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj


class KafkaSqlRepository(SqlRepository[T], KafkaTopicMixin):
    def __init__(
        self,
        model: Type[T],
        session: AsyncSession,
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
