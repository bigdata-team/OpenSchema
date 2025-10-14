from fastapi import APIRouter

from common.connection.kafka import AsyncKafkaConnection
from common.connection.mongo import AsyncMongoConnection
from common.connection.neo4j import AsyncNeo4jConnection
from common.connection.postgres import AsyncPostgresConnection
from common.connection.redis import AsyncRedisConnection
from common.connection.s3 import AsyncS3Connection
from common.model.http import create_response

router = APIRouter(tags=["public"])


@router.get("/ping")
async def ping():
    return create_response("pong")


@router.get("/healthz")
async def healthz():
    results = {}
    for name, cls in {
        "kafka": AsyncKafkaConnection,
        "redis": AsyncRedisConnection,
        "postgres": AsyncPostgresConnection,
        "neo4j": AsyncNeo4jConnection,
        "mongo": AsyncMongoConnection,
        "s3": AsyncS3Connection,
    }.items():
        try:
            await cls().connect()
            results[name] = "success"
        except Exception as e:
            results[name] = f"error: {str(e)}"
    return create_response(data=results)
