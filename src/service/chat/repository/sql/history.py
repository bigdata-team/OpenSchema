from fastapi import Depends
from sqlmodel import select

from common.connection import get_session
from common.connection.kafka import KafkaConnection
from common.connection.sql import PostgresConnection
from common.middleware.correlation import get_crid
from common.repository.sql import KafkaSqlRepository
from model.sql.history import History


class HistoryRepository(KafkaSqlRepository[History]):
    def __init__(
        self,
        sql=Depends(get_session(PostgresConnection)),
        kafka=Depends(get_session(KafkaConnection)),
        crid=Depends(get_crid()),
    ):
        super().__init__(model=History, sql=sql, kafka=kafka, crid=crid)
