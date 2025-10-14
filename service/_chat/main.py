import json
import os

import httpx
from common.chat import Handler
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse
from models.db import *
from sqlalchemy import text

from common.lifespan import compose, kafka, postgres
from common.middleware import *

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI(
    root_path="/api/v1/chat",
    lifespan=compose(kafka, postgres),
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
    return create_response("Ok", "Chat service is healthy.", None, 200)


class MyHander(Handler):
    def __init__(self, url, headers, body, app, request, tasks):
        super().__init__(url, headers, body, app, request, tasks)

    async def stream_parser(self, content):
        chunks = super().stream_parser(content)
        meta = chunks[-1]
        await self.store(chunks, meta)

    async def nonstream_parser(self, content):
        content = super().nonstream_parser(content)
        meta = content
        await self.store(content, meta)

    async def store(self, content: str, meta: dict):
        async with self.app.state.postgres_session() as db:
            history = History(
                user_id=(
                    self.request.state.token.sub if self.request.state.token else None
                ),
                service_id=self.request.headers.get("X-Service-Id"),
                model_name=meta.get("model"),
                url=self.url,
                request=json.dumps(self.body),
                response=json.dumps(content),
                tokens=meta.get("usage").get("total_tokens"),
            )
            db.add(history)
            await db.commit()


@app.post("/completions")
@identify
async def chat_proxy(request: Request, tasks: BackgroundTasks):
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    body = await request.json()
    handler = MyHander(url, headers, body, app, request, tasks)
    return await handler.run()
