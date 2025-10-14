from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from router import private_router, public_router

from common.config import PROJECT_NAME, SERVICE_API_VERSION, SERVICE_NAME
from common.connection.kafka import KafkaConnection
from common.connection.mongo import MongoConnection
from common.connection.redis import RedisConnection
from common.connection.s3 import S3Connection
from common.connection.sql import PostgresConnection
from common.lifespan import compose
from common.middleware import CorrelationIdMiddleware

lifespan = compose(
    PostgresConnection, MongoConnection, RedisConnection, KafkaConnection, S3Connection
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


# @app.get("/test")
# async def test():
#     from common.celery.job import greet
#     from job import add

#     from celery import chain

#     tasks = chain(greet.s("***********"), add.s(23))
#     result = tasks.apply_async()

#     return {"message": "This is a test endpoint.", "celery_task_id": result.id}


# from celery.result import AsyncResult
# from common.celery.worker import worker


# @app.get("/jobs/{task_id}")
# async def get_job_status(task_id: str):
#     # Ensure we query the SAME Celery app/backend as the worker
#     result = AsyncResult(task_id, app=worker)
#     return {
#         "task_id": task_id,
#         "state": result.state,
#         "status": result.status,
#         "ready": result.ready(),
#         "successful": (result.successful() if result.ready() else False),
#         "result": (result.result if result.ready() else None),
#     }


from model.sql import User as U1

from common.repository.sql import create_kafka_postgres_repo, create_postgres_repo


@app.get("/pgrepo")
async def pgrepo(repo=Depends(create_kafka_postgres_repo(U1))):

    result = await repo.create(U1())
    return result


from model.mongo import User as U2

from common.repository.mongo import create_kafka_mongo_repo, create_mongo_repo


@app.get("/mongorepo")
async def mongorepo(repo=Depends(create_kafka_mongo_repo(U2))):

    result = await repo.create(U2())
    return result


from common.repository.redis import create_redis_repo


@app.get("/redisrepo")
async def redisrepo(repo=Depends(create_redis_repo(U2))):

    result = await repo.create_or_update("someid", U2())
    return result


from fastapi import File, UploadFile

from common.repository.s3 import create_s3_repo


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), repo=Depends(create_s3_repo())):
    contents = await file.read()
    id = file.filename
    result = await repo.create_or_update(id, contents)
    return {"filename": id}
