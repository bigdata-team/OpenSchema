from typing import Type, TypeVar

from neo4j import AsyncSession

from .repository import Repository

T = TypeVar("T")


class Neo4jRepository(Repository[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        super().__init__(model, session)
        self.session: AsyncSession

    async def connect(self, crid: str | None = None) -> None:
        await self.session.run("RETURN 1")

    async def create(self, obj: T, crid: str | None = None) -> T:
        raise NotImplementedError

    async def get(self, id: str, crid: str | None = None) -> T | None:
        raise NotImplementedError

    async def update(self, id: str, obj: T, crid: str | None = None) -> T | None:
        raise NotImplementedError

    async def delete(self, id: str, crid: str | None = None) -> T | None:
        raise NotImplementedError
