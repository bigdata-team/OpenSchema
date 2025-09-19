from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from sqlalchemy import text

from common.lifespan import compose, kafka, neo4j, postgres, redis, s3
from common.log import create_logger
from common.middleware import CorrelationIdMiddleware
from common.model.event import Envelope
from common.model.http import create_response
from common.model.log import Log

logger = create_logger(name="template")

app = FastAPI(
    root_path="/api/v1/template",
    lifespan=compose(kafka, postgres, redis, s3, neo4j),
)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz(request: Request):
    logger.debug(Log().model_dump_json())

    e = Envelope(event="template.healthz", crid=request.state.crid)
    await app.state.kafka_producer.send_and_wait(
        topic=e.event, value=e.model_dump_json().encode()
    )

    async with app.state.postgres_session() as session:
        await session.execute(text("SELECT 1"))

    await app.state.redis.ping()

    await app.state.s3.list_buckets()

    async with app.state.neo4j.session() as session:
        await session.run("RETURN 1")

    return create_response("ok", request.state.crid)
