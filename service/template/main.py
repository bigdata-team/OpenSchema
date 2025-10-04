import os

from fastapi import FastAPI
import asyncio
from starlette.concurrency import run_in_threadpool
from fastapi.openapi.utils import get_openapi
from router import private_router, public_router

from common.middleware import CorrelationIdMiddleware

SERVICE_ID = os.getenv("SERVICE_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME", "")

app = FastAPI(
    title="FastAPI",
    description=f"{SERVICE_NAME.title()} service",
    version="1.0.0",
    root_path=f"/api/v1/{SERVICE_NAME}",
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
