from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from router import private_router, public_router

from common.config import PROJECT_NAME, SERVICE_API_VERSION, SERVICE_NAME
from common.lifespan import compose
from common.lifespan.kafka import create_kafka_lifespan, get_kafka_session
from common.lifespan.mongo import create_mongo_lifespan, get_mongo_session
from common.lifespan.redis import create_redis_lifespan, get_redis_session
from common.lifespan.neo4j import create_neo4j_lifespan, get_neo4j_session
from common.lifespan.s3 import create_s3_lifespan, get_s3_session
from common.lifespan.sql.postgres import create_postgres_lifespan, get_postgres_session
from common.middleware import CorrelationIdMiddleware

lifespan = compose(
    create_postgres_lifespan(),
    create_mongo_lifespan(),
    create_kafka_lifespan(),
    create_redis_lifespan(),
    create_neo4j_lifespan(),
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


@app.get("/test")
async def test():
    from common.celery.job import greet
    from job import add

    from celery import chain

    tasks = chain(greet.s("***********"), add.s(23))
    result = tasks.apply_async()

    return {"message": "This is a test endpoint.", "celery_task_id": result.id}


from celery.result import AsyncResult
from common.celery.worker import worker


@app.get("/jobs/{task_id}")
async def get_job_status(task_id: str):
    # Ensure we query the SAME Celery app/backend as the worker
    result = AsyncResult(task_id, app=worker)
    return {
        "task_id": task_id,
        "state": result.state,
        "status": result.status,
        "ready": result.ready(),
        "successful": (result.successful() if result.ready() else False),
        "result": (result.result if result.ready() else None),
    }
