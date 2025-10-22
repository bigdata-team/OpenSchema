from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from router import private_router, protected_router, public_router
from starlette.middleware.cors import CORSMiddleware

from common.config import PROJECT_NAME, SERVICE_VERSION, SERVICE_NAME
from common.connection.kafka import KafkaConnection
from common.connection.sql import PostgresConnection
from common.util.lifespan import compose
from common.middleware import CorrelationIdMiddleware

pg = PostgresConnection()
kafka = KafkaConnection()

lifespan = compose(PostgresConnection, KafkaConnection)

app = FastAPI(
    title=PROJECT_NAME,
    version=SERVICE_VERSION,
    root_path=f"/api/{SERVICE_VERSION}/{SERVICE_NAME}",
    lifespan=lifespan,
)

app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router, prefix="")
app.include_router(private_router, prefix="")
app.include_router(protected_router, prefix="")


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
