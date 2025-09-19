from contextlib import AsyncExitStack, asynccontextmanager


def compose(*lifespans):
    @asynccontextmanager
    async def combined(app):
        async with AsyncExitStack() as stack:
            for lifespan in lifespans:
                await stack.enter_async_context(lifespan(app))
            yield

    return combined


def init_schema(engine):
    from .models.db import create_schema as create_schema

    @asynccontextmanager
    async def lifespan(app):
        await create_schema(engine)
        yield

    return lifespan


@asynccontextmanager
async def kafka(app):
    from .connection.kafka import create_kafka_producer

    producer = create_kafka_producer()
    await producer.start()
    app.state.kafka_producer = producer
    try:
        yield
    finally:
        await producer.stop()


@asynccontextmanager
async def postgres(app):
    from .connection.postgres import SessionLocal, engine

    app.state.postgres_session = SessionLocal
    try:
        yield
    finally:
        await engine.dispose()


@asynccontextmanager
async def redis(app):
    from .connection.redis import get_redis

    redis_client = await get_redis()
    app.state.redis = redis_client
    try:
        yield
    finally:
        await redis_client.close()


@asynccontextmanager
async def s3(app):
    from .connection.s3 import get_s3

    session = get_s3()
    s3_client = await session.__aenter__()
    app.state.s3 = s3_client
    try:
        yield
    finally:
        await s3_client.__aexit__(None, None, None)


@asynccontextmanager
async def neo4j(app):
    from .connection.neo4j import get_neo4j

    driver = get_neo4j()
    app.state.neo4j = driver
    try:
        yield
    finally:
        await driver.close()
