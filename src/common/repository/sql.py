from datetime import datetime
from typing import Type, TypeVar

from aiokafka import AIOKafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, text

from common.model.sql import BaseOrm
from common.repository import Repository
from common.repository.kafka import KafkaMixin

T = TypeVar("T", bound=BaseOrm)


class SqlRepository(Repository[T]):
    def __init__(self, model: Type[T], sql: AsyncSession):
        super().__init__(model)
        self.sql: AsyncSession = sql

    async def connect(self) -> None:
        (await self.sql.execute(text("SELECT 1"))).scalar_one()

    async def create(self, obj: T) -> T:
        self.sql.add(obj)
        await self.sql.commit()
        await self.sql.refresh(obj)
        return obj

    async def get(self, id: str) -> T | None:
        query = select(self.model).where(
            self.model.id == id, self.model.deleted_at == None
        )
        result = await self.sql.execute(query)
        return result.scalar_one_or_none()

    async def update(self, id: str, obj: T) -> T | None:
        prev_obj = await self.get(id)
        if not prev_obj:
            return None
        for key, value in obj.model_dump(
            exclude_unset=True,
            exclude={"id", "seq", "created_at", "updated_at", "deleted_at"},
        ).items():
            setattr(prev_obj, key, value)
        await self.sql.commit()
        await self.sql.refresh(prev_obj)
        return prev_obj

    async def delete(self, id: str) -> T | None:
        obj = await self.get(id)
        if not obj:
            return None
        obj.deleted_at = datetime.now()
        await self.sql.commit()
        await self.sql.refresh(obj)
        return obj


class KafkaSqlRepository(SqlRepository[T], KafkaMixin):
    def __init__(
        self, model: Type[T], sql: AsyncSession, kafka: AIOKafkaProducer, crid: str
    ) -> None:
        SqlRepository.__init__(self, model=model, sql=sql)
        KafkaMixin.__init__(self, model=model, kafka=kafka, crid=crid)

    async def connect(self) -> None:
        await SqlRepository.connect(self)
        await self.publish_event(payload={"event": "connected"}, action="connected")

    async def create(self, obj: T) -> T:
        obj = await SqlRepository.create(self, obj)
        if obj:
            await self.publish_event(payload=obj.model_dump(), action="created")
        return obj

    async def get(self, id: str) -> T | None:
        obj = await SqlRepository.get(self, id)
        if obj:
            await self.publish_event(payload=obj.model_dump(), action="retrieved")
        return obj

    async def update(self, id: str, obj: T) -> T | None:
        obj = await SqlRepository.update(self, id, obj)
        if obj:
            await self.publish_event(payload=obj.model_dump(), action="updated")
        return obj

    async def delete(self, id: str) -> T | None:
        obj = await SqlRepository.delete(self, id)
        if obj:
            await self.publish_event(payload=obj.model_dump(), action="deleted")
        return obj


def create_postgres_repo(model: Type[T]) -> callable:
    from fastapi import Depends

    from common.connection import get_session
    from common.connection.sql import PostgresConnection

    def _get_repo(sql=Depends(get_session(PostgresConnection))):
        return SqlRepository(model=model, sql=sql)

    return _get_repo


def create_kafka_postgres_repo(model: Type[T]) -> callable:
    from fastapi import Depends

    from common.connection import get_session
    from common.connection.kafka import KafkaConnection
    from common.connection.sql import PostgresConnection
    from common.middleware.correlation import get_crid

    def _get_repo(
        sql=Depends(get_session(PostgresConnection)),
        kafka=Depends(get_session(KafkaConnection)),
        crid=Depends(get_crid()),
    ):
        return KafkaSqlRepository(model=model, sql=sql, kafka=kafka, crid=crid)

    return _get_repo
