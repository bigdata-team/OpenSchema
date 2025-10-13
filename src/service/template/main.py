from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from router import private_router, public_router

from common.config import PROJECT_NAME, SERVICE_API_VERSION, SERVICE_NAME
from common.lifespan import compose
from common.lifespan.kafka import create_kafka_lifespan, get_kafka_session
from common.lifespan.mongo import create_mongo_lifespan, get_mongo_session
from common.lifespan.redis import create_redis_lifespan, get_redis_session
from common.lifespan.s3 import create_s3_lifespan, get_s3_session
from common.lifespan.sql.postgres import create_postgres_lifespan, get_postgres_session
from common.middleware import CorrelationIdMiddleware

lifespan = compose(
    create_postgres_lifespan(),
    create_mongo_lifespan(),
    create_kafka_lifespan(),
    create_redis_lifespan(),
    create_s3_lifespan(),
)

app = FastAPI(
    title=PROJECT_NAME,
    version=SERVICE_API_VERSION,
    root_path=f"/api/{SERVICE_API_VERSION}/{SERVICE_NAME}",
    lifespan=lifespan,
)

app.add_middleware(CorrelationIdMiddleware)

app.include_router(public_router, prefix="")
app.include_router(private_router, prefix="")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    server_url = app.root_path
    openapi_schema["servers"] = [{"url": server_url}]
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Use jwt access token for authorization",
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


from fastapi import File, UploadFile
from model.sql import User

from common.repository.mongo import (
    KafkaMongoRepository,
    MongoRepository,
    create_kafka_mongo_repo,
    create_mongo_repo,
)
from common.repository.redis import RedisRepository, create_redis_repo
from common.repository.s3 import S3Repository, create_s3_repo
from common.repository.sql import KafkaSqlRepository
from common.repository.sql.postgres import (
    create_kafka_postgres_repo,
    create_postgres_repo,
)

# from model.mongo import User


@app.get("/delete")
async def delete(
    repo: S3Repository = Depends(create_s3_repo()),
):
    await repo.delete("참여 동기.docx")


@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    repo: S3Repository = Depends(create_s3_repo()),
):
    contents = await file.read()
    result = await repo.create_or_update(file.filename, contents)
    return {"message": "ok"}
