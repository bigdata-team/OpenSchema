from typing import Type, TypeVar

from fastapi import Depends

from common.lifespan import get_crid
from common.lifespan.kafka import get_kafka_session
from common.lifespan.sql.postgres import get_postgres_session
from common.repository.sql import KafkaSqlRepository, SqlRepository

T = TypeVar("T")


def create_postgres_repo(model: Type[T]) -> callable:
    def _get_repo(
        sql=Depends(get_postgres_session()),
    ) -> SqlRepository[T]:
        return SqlRepository(model=model, sql=sql)

    return _get_repo


def create_kafka_postgres_repo(model: Type[T]) -> callable:
    def _get_repo(
        sql=Depends(get_postgres_session()),
        kafka=Depends(get_kafka_session()),
        crid=Depends(get_crid()),
    ) -> KafkaSqlRepository[T]:
        return KafkaSqlRepository(model=model, sql=sql, kafka=kafka, crid=crid)

    return _get_repo
