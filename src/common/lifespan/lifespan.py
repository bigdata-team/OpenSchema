from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import Request


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
