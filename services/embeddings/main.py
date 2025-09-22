import json
import os

import httpx
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from models.db import *
from sqlalchemy import text

from common.lifespan import compose, kafka, postgres
from common.middleware import *
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    root_path="/api/v1/embeddings",
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
    return create_response("Ok", "Embedding service is healthy.", None, 200)


async def task(app, request, response, url):
    content = json.loads(response.content)

    async with app.state.postgres_session() as db:
        history = History(
            user_id=(request.state.token.sub if request.state.token else None),
            service_id=request.headers.get("X-Service-Id", None),
            model_name=content.get("model"),
            url=url,
            request=json.dumps(json.loads(await request.body())),
            response=json.dumps(content),
            tokens=content.get("usage").get("total_tokens"),
        )
        db.add(history)
        await db.commit()


@app.post("")
@identify
async def embeddings_proxy(request: Request, tasks: BackgroundTasks):
    url = f"{OPENAI_BASE_URL}/embeddings"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    body = json.loads(await request.body())

    async with httpx.AsyncClient(timeout=60) as client:
        res = await client.post(url, headers=headers, json=body)

    tasks.add_task(task, app=app, request=request, response=res, url=url)

    return Response(
        content=res.content,
        status_code=res.status_code,
        media_type=res.headers.get("content-type"),
    )
