from typing import Any, TypeVar

from aiokafka import AIOKafkaProducer
from common.connection import get_session
from common.connection.kafka import KafkaSession
from common.const import SERVICE_DB_SCHEMA
from fastapi import Depends

from common.model.kafka import BaseEvent

from .repository import Repository


class KafkaRepository(Repository[BaseEvent]):
    def __init__(self, session: AIOKafkaProducer):
        super().__init__(BaseEvent, session)

    async def connect(self, crid: str | None = None) -> None:
        topic = "connect"
        event = BaseEvent(topic=topic, payload=None, crid=crid)
        await self.session.send_and_wait(topic, event.model_dump_json().encode())

    async def create(self, obj: BaseEvent, crid: str | None = None) -> BaseEvent:
        obj.crid = crid or obj.crid
        await self.session.send_and_wait(obj.topic, obj.model_dump_json().encode())
        return obj

    async def create_event(
        self, topic: str, payload: Any, crid: str | None = None
    ) -> BaseEvent:
        event = BaseEvent(topic=topic, payload=payload, crid=crid)
        return await self.create(event, crid=crid)


T = TypeVar("T")


class KafkaTopicMixin:
    def create_kafka_topic(self, action: str) -> str:
        return f"{SERVICE_DB_SCHEMA}.{self.model.__name__.lower()}.{action}"


def get_kafka_repodep() -> callable:
    async def _get_repo(
        session: AIOKafkaProducer = Depends(get_session(KafkaSession)),
    ) -> KafkaRepository:
        return KafkaRepository(session)

    return _get_repo
