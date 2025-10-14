from typing import Type, TypeVar

from neo4j import AsyncSession

from common.repository import Repository

T = TypeVar("T")


class Neo4jRepository(Repository[T]):
    def __init__(self, model: Type[T], neo4j: AsyncSession):
        super().__init__(model)
        self.neo4j: AsyncSession = neo4j

    async def connect(self) -> None:
        await self.neo4j.run("RETURN 1")


def create_neo4j_repository(model: Type[T]):
    from fastapi import Depends

    from common.connection import get_session
    from common.connection.neo4j import Neo4jConnection

    async def _unpack(neo4j=Depends(get_session(Neo4jConnection))):
        return Neo4jRepository(model=model, neo4j=neo4j)

    return _unpack
