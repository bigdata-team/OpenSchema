import asyncio
import time
import uuid
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI, Request


def compose(*lifespans):
    @asynccontextmanager
    async def composed_lifespan(app):
        async with AsyncExitStack() as stack:
            for lifespan in lifespans:
                await stack.enter_async_context(lifespan(app))
            yield

    return composed_lifespan


def get_crid():
    async def _unpack(request: Request) -> str | None:
        crid = request.state.crid or None
        return crid

    return _unpack


class Runner:
    def __init__(self):
        self.futures = []

    def add(self, func: callable, *args, **kwargs):
        self.futures.append((func, args, kwargs))

    async def run(self):
        for func, args, kwargs in self.futures:
            if asyncio.iscoroutinefunction(func):
                await func(*args, **kwargs)
            else:
                func(*args, **kwargs)


class Lifespan:
    def __init__(self, name: str = "lifespan"):
        self.name: str = name
        self.key: str = str(uuid.uuid4())
        self.created_at: float = time.time()
        self.state: dict = {}

        self.on_startup = Runner()
        self.on_shutdown = Runner()

    def add_startup(self, func: callable, *args, **kwargs):
        self.on_startup.add(func, *args, **kwargs)

    def add_shutdown(self, func: callable, *args, **kwargs):
        self.on_shutdown.add(func, *args, **kwargs)

    def add_context(self, contextmanager):
        if hasattr(contextmanager, "__aenter__") and hasattr(
            contextmanager, "__aexit__"
        ):
            futures = self.on_startup.futures
            self.on_startup.futures = [(contextmanager.__aenter__, (), {}), *futures]

            futures = self.on_shutdown.futures
            self.on_shutdown.futures = [*futures, (contextmanager.__aexit__, (), {})]
        elif hasattr(contextmanager, "__enter__") and hasattr(
            contextmanager, "__exit__"
        ):
            futures = self.on_startup.futures
            self.on_startup.futures = [
                (contextmanager.__enter__, (), {}),
                *futures,
            ]

            futures = self.on_shutdown.futures
            self.on_shutdown.futures = [*futures, (contextmanager.__exit__, (), {})]

    async def __aenter__(self):
        await self.on_startup.run()
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        await self.on_shutdown.run()

    async def lifespan(self, app: FastAPI):
        await self.__aenter__()
        yield self.state
        await self.__aexit__(None, None, None)
