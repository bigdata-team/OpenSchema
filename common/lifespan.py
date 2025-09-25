from contextlib import AsyncExitStack, asynccontextmanager


def compose(*lifespans):
    @asynccontextmanager
    async def combined(app):
        async with AsyncExitStack() as stack:
            for lifespan in lifespans:
                await stack.enter_async_context(lifespan(app))
            yield

    return combined


@asynccontextmanager
async def kafka(app):
    from .connection.kafka import create_aiokafka_producer

    producer = create_aiokafka_producer()
    await producer.start()
    app.state.kafka_producer = producer
    try:
        yield
    finally:
        await producer.stop()


@asynccontextmanager
async def postgres(app):
    from .connection.postgres import SessionLocal, engine
    from .models.db import _Base

    async def create_schema(engine):
        async with engine.begin() as conn:
            await conn.run_sync(_Base.metadata.create_all)

    await create_schema(engine)

    app.state.postgres_session = SessionLocal
    try:
        yield
    finally:
        await engine.dispose()


@asynccontextmanager
async def mongo(app):
    from beanie import init_beanie
    from motor.motor_asyncio import AsyncIOMotorClient

    from .connection.mongo import MONGO_DB, MONGO_URI, get_aiomongo
    from .models.mongo import Base

    async def create_schema():
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB]
        await init_beanie(database=db, document_models=[Base])

    await create_schema()

    db = await get_aiomongo()
    app.state.mongo = db
    try:
        yield
    finally:
        db.client.close()


@asynccontextmanager
async def redis(app):
    from .connection.redis import get_aioredis

    redis_client = await get_aioredis()
    app.state.redis = redis_client
    try:
        yield
    finally:
        await redis_client.close()


@asynccontextmanager
async def s3(app):
    from .connection.s3 import get_aios3

    async with get_aios3() as s3:
        app.state.s3 = s3
        yield


@asynccontextmanager
async def neo4j(app):
    from .connection.neo4j import get_aioneo4j

    driver = get_aioneo4j()
    app.state.neo4j = driver
    try:
        yield
    finally:
        await driver.close()
