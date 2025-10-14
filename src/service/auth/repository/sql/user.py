from fastapi import Depends
from model.sql import User
from sqlmodel import select

from common.connection import get_session
from common.connection.kafka import KafkaConnection
from common.connection.sql import PostgresConnection
from common.middleware.correlation import get_crid
from common.repository.sql import KafkaSqlRepository


class UserRepository(KafkaSqlRepository[User]):
    def __init__(
        self,
        sql=Depends(get_session(PostgresConnection)),
        kafka=Depends(get_session(KafkaConnection)),
        crid=Depends(get_crid()),
    ):
        super().__init__(model=User, sql=sql, kafka=kafka, crid=crid)

    async def get_by_email(self, email: str) -> User | None:
        query = select(self.model).where(
            self.model.email == email, self.model.deleted_at == None
        )
        result = await self.sql.execute(query)
        return result.scalar_one_or_none()
