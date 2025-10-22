from contextlib import AsyncExitStack, asynccontextmanager

def compose(*lifespans):
    @asynccontextmanager
    async def composed_lifespan(app):
        async with AsyncExitStack() as stack:
            for lifespan in lifespans:
                await stack.enter_async_context(lifespan(app))
            yield

    return composed_lifespan
