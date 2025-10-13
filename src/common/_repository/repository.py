from abc import abstractmethod
from typing import Any, Generic, Type, TypeVar

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, model: Type[T], session: Any):
        self.model = model
        self.session = session

    @abstractmethod
    async def connect(self, crid: str | None = None) -> None:
        pass

    async def create(self, obj: T, crid: str | None = None) -> T:
        raise NotImplementedError

    async def get(self, id: str, crid: str | None = None) -> T | None:
        raise NotImplementedError

    async def update(self, id: str, obj: T, crid: str | None = None) -> T | None:
        raise NotImplementedError

    async def delete(self, id: str, crid: str | None = None) -> T | None:
        raise NotImplementedError
