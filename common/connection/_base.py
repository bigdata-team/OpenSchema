import inspect
import os
import threading
import time
from abc import ABC, abstractmethod
from typing import TypeVar

TSession = TypeVar("TSession")


def unpack(method):

    def wrapper(self, *args, **kwargs):
        self.__enter__()
        try:
            return method(self, *args, **kwargs)
        finally:
            self.__exit__()

    async def awrapper(self, *args, **kwargs):
        await self.__aenter__()
        try:
            return await method(self, *args, **kwargs)
        finally:
            await self.__aexit__()

    if inspect.iscoroutinefunction(method):
        return awrapper
    return wrapper


class Connection(ABC):
    def __init__(self, id: str):
        self.id = id
        self.session: TSession | None = None

    def __enter__(self) -> TSession:
        raise NotImplementedError

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        raise NotImplementedError

    @unpack
    def connect(self):
        raise NotImplementedError


class AsyncConnection(ABC):
    def __init__(self, id: str):
        self.id = id
        self.session: TSession | None = None

    async def __aenter__(self) -> TSession:
        raise NotImplementedError

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        raise NotImplementedError

    @unpack
    async def connect(self):
        raise NotImplementedError


class Registry:
    _registry: dict[str, any] = {}
    _lock = threading.Lock()

    @classmethod
    def register(cls, key: str, value: any):
        with cls._lock:
            cls._registry[key] = value
            cls._registry[key]["__created_at__"] = time.time()

    @classmethod
    def has(cls, key: str) -> bool:
        return key in cls._registry

    @classmethod
    def get(cls, key: str):
        return cls._registry.get(key, None)

    @classmethod
    def dispose(cls, key: str):
        with cls._lock:
            if key in cls._registry:
                del cls._registry[key]
