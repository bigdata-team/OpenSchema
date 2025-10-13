from abc import abstractmethod
from typing import Any, Generic, Type, TypeVar

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    @abstractmethod
    async def connect(self) -> None:
        pass

    async def create(self, obj: T) -> T:
        raise NotImplementedError

    async def get(self, id: str) -> T | None:
        raise NotImplementedError

    async def update(self, id: str, obj: T) -> T | None:
        raise NotImplementedError

    async def delete(self, id: str) -> T | None:
        raise NotImplementedError
