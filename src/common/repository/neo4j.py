from common.lifespan.neo4j import get_neo4j_session
from fastapi import Depends
from typing import Type, TypeVar
from common.repository import Repository
from neo4j import AsyncSession

T = TypeVar("T")


class Neo4jRepository(Repository[T]):
    def __init__(self, model: Type[T], neo4j: AsyncSession):
        super().__init__(model)
        self.neo4j: AsyncSession = neo4j

    async def connect(self) -> None:
        await self.neo4j.run("RETURN 1")


def create_neo4j_repository(model: Type[T]):
    async def _unpack(neo4j: AsyncSession = Depends(get_neo4j_session())):
        return Neo4jRepository[model](model, neo4j)

    return _unpack
