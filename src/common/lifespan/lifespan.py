from contextlib import asynccontextmanager

from fastapi import Request


def compose(*lifespans):
    @asynccontextmanager
    async def composed_lifespan(app):
        for lifespan in lifespans:
            await lifespan(app).__aenter__()
        yield
        for lifespan in reversed(lifespans):
            await lifespan(app).__aexit__(None, None, None)

    return composed_lifespan


def get_crid():
    async def _unpack(request: Request) -> str | None:
        crid = request.state.crid or None
        return crid

    return _unpack
