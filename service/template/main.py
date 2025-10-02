import os
from fastapi import FastAPI
from controller import internal_router, private_router, public_router

SERVICE_ID = os.getenv("SERVICE_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME")

app = FastAPI(
    title="FastAPI",
    description=f"{SERVICE_NAME.title()} service",
    version="1.0.0",
    root_path=f"/api/v1",
)

app.include_router(public_router, prefix=f"/public/{SERVICE_NAME}")
app.include_router(private_router, prefix=f"/{SERVICE_NAME}")
app.include_router(internal_router, prefix=f"/internal/{SERVICE_NAME}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
