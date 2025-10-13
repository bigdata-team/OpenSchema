from typing import Type, TypeVar

from aiokafka import AIOKafkaProducer

from common.config.const import SERVICE_DB_SCHEMA
from common.model.kafka import BaseEvent

T = TypeVar("T")


class KafkaMixin:
    def __init__(self, model: Type[T], kafka: AIOKafkaProducer, crid: str):
        self.model = model
        self.kafka = kafka
        self.crid = crid

    @property
    def topic_base(self) -> str:
        return f"{SERVICE_DB_SCHEMA}.{self.model.__name__.lower()}"

    def create_topic_name(self, action: str | None = None) -> str:
        if action:
            return f"{self.topic_base}.{action}"
        return self.topic_base

    async def publish_event(self, payload: any, action: str | None = None) -> BaseEvent:
        event = BaseEvent(
            topic=self.create_topic_name(action), payload=payload, crid=self.crid
        )
        await self.kafka.send_and_wait(event.topic, event.model_dump_json().encode())
        return event
