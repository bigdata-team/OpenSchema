import json
import os

import httpx
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse, JSONResponse
from models.db import *
from models.http import *
from sqlalchemy import text

from common.chat import Handler
from common.connection.postgres import engine
from common.lifespan import compose, init_schema, kafka, postgres
from common.middleware import *
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    root_path="/api/v1/embeddings",
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
    return create_response(
        "Ok", "Embedding service is healthy.", request.state.crid, 200
    )


@app.post("")
# @protected
async def embeddings_proxy(request: Request):
    url = f"{OPENAI_API_KEY}/embeddings"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    body = await request.body()

    async with httpx.AsyncClient(timeout=60) as client:
        res = await client.post(url, headers=headers, content=body)
    
    print("**************")
    print(res)
    print("**************")

    return JSONResponse(status_code=res.status_code, content=res.json())

