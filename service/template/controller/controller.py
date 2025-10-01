import os

from fastapi import FastAPI

from common.controller import create_healthz, ping
from common.repository import *

from service.info import InfoService

SERVICE_ID = os.getenv("SERVICE_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME")


healthz = create_healthz(
    repositories=[
        PostgresRepository(),
        AsyncPostgresRepository(),
        AsyncMongoRepository(),
        Neo4jRepository(),
        AsyncNeo4jRepository(),
        S3Repository(),
        AsyncS3Repositry(),
        RedisRepository(),
        AsyncRedisRepository(),
        AsyncKafkaRepository(),
    ]
)


app = FastAPI(root_path=f"/api/v1/{SERVICE_NAME}")
app.get("/ping")(ping)
app.get("/healthz")(healthz)

@app.get("/info")
def info():
    svc = InfoService()
    return svc.info() 