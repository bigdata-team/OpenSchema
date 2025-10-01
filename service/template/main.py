import os

from fastapi import FastAPI


SERVICE_ID = os.getenv("SERVICE_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME")


app = FastAPI(
    root_path=f"/api/v1/{SERVICE_NAME}"
)

app.add_routes