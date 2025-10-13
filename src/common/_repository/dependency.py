from typing import Type, TypeVar

from common.connection import get_session
from fastapi import Depends
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
TS = TypeVar("TS", bound=BaseModel | str)


def get_redis_repo(model: Type[TS]) -> callable:
    import redis
    from common.connection.redis import RedisSession

    from common._repository.redis import RedisRepository

    async def _get_repo(
        session: redis.asyncio.Redis = Depends(get_session(RedisSession)),
    ) -> RedisRepository[T]:
        return RedisRepository(model, session)

    return _get_repo


def get_postgres_repo(model: Type[T]):
    from common.connection.sql.postgres import PostgresSession
    from sqlalchemy.ext.asyncio import AsyncSession

    from common._repository.sql import SqlRepository

    async def _get_repo(
        session: AsyncSession = Depends(get_session(PostgresSession)),
    ) -> SqlRepository[T]:
        return SqlRepository(model, session)

    return _get_repo


def get_kafka_postgres_repo(model: Type[T]):
    from aiokafka import AIOKafkaProducer
    from common.connection.kafka import KafkaSession
    from common.connection.sql.postgres import PostgresSession
    from sqlalchemy.ext.asyncio import AsyncSession

    from common._repository.sql import KafkaSqlRepository

    async def _get_repo(
        session: AsyncSession = Depends(get_session(PostgresSession)),
        kafka_session: AIOKafkaProducer = Depends(get_session(KafkaSession)),
    ) -> KafkaSqlRepository[T]:
        return KafkaSqlRepository(model, session, kafka_session)

    return _get_repo


def get_mongo_repo(model: Type[T]) -> callable:
    from common.connection.mongo import MongoSession
    from motor.motor_asyncio import AsyncIOMotorDatabase

    from common._repository.mongo import MongoRepository

    async def _get_repo(
        session: AsyncIOMotorDatabase = Depends(get_session(MongoSession)),
    ) -> MongoRepository[T]:
        return MongoRepository(model, session)

    return _get_repo


def get_kafka_mongo_repo(model: Type[T]) -> callable:
    from aiokafka import AIOKafkaProducer
    from common.connection.kafka import KafkaSession
    from common.connection.mongo import MongoSession
    from motor.motor_asyncio import AsyncIOMotorDatabase

    from common._repository.mongo import KafkaMongoRepository

    async def _get_repo(
        session: AsyncIOMotorDatabase = Depends(get_session(MongoSession)),
        kafka_session: AIOKafkaProducer = Depends(get_session(KafkaSession)),
    ) -> KafkaMongoRepository[T]:
        return KafkaMongoRepository(model, session, kafka_session)

    return _get_repo


def get_neo4j_repo(model: Type[T]) -> callable:
    from common.connection.neo4j import Neo4jSession
    from neo4j import AsyncSession

    from common._repository.neo4j import Neo4jRepository

    async def _get_repo(
        session: AsyncSession = Depends(get_session(Neo4jSession)),
    ) -> Neo4jRepository[T]:
        return Neo4jRepository(model, session)

    return _get_repo
