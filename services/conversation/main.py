import json
import os

import httpx
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse
from models.db import *
from sqlalchemy import text

from common.chat import Handler
from common.connection.postgres import engine
from common.lifespan import compose, init_schema, kafka, postgres
from common.middleware import *
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response

SERVICE_NAME = os.getenv("SERVICE_NAME")
SERVICE_ID = os.getenv("SERVICE_ID")

app = FastAPI(
    root_path="/api/v1/conversation",
    lifespan=compose(init_schema(engine), kafka, postgres),
)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz(request: Request):
    async with app.state.postgres_session() as session:
        await session.execute(text("SELECT 1"))
    return create_response("Ok", "Conversation service is healthy.", None, 200)


class MyHander(Handler):
    def __init__(self, url, headers, body, app, request, tasks):
        super().__init__(url, headers, body, app, request, tasks)

    def stream_parser(self, content):
        chunks = super().stream_parser(content)

    def nonstream_parser(self, content):
        content = super().nonstream_parser(content)


@app.post("")
@protected
async def conversation(request: Request, tasks: BackgroundTasks):
    url = "http://chat:8000/api/v1/chat/completions"
    headers = dict(request.headers)
    headers["X-Service-Id"] = SERVICE_ID
    body = await request.json()

    handler = MyHander(url, headers, body, app, request, tasks)
    return await handler.run()
