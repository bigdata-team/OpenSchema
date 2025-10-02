import os
from fastapi import FastAPI
from controller import router
from common.middleware import CorrelationIdMiddleware, AuthenticationMiddleware

SERVICE_ID = os.getenv("SERVICE_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME")

app = FastAPI(
    title="FastAPI",
    description=f"{SERVICE_NAME.title()} service",
    version="1.0.0",
    root_path=f"/api/v1/{SERVICE_NAME}",
)

app.add_middleware(AuthenticationMiddleware)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
