from fastapi import FastAPI

from common.lifespan import compose, init_schema, kafka, postgres
from common.models.http import create_response, DataResponseModel
from common.models.event import create_event
from common.middleware import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from sqlalchemy import text
from models.http import *
from models.db import *
from common.connection.postgres import engine
from common.jwt import JWTService
from fastapi import Depends
from fastapi.responses import StreamingResponse, Response
from common.jwt import get_tokens
import httpx
import json
import os

jwt = JWTService()

app = FastAPI(
    root_path="/api/v1/proxy",
    lifespan=compose(init_schema(engine), kafka, postgres),
)
app.add_middleware(XTransactionIdMiddleware)
app.add_middleware(XServiceIdMiddleware)
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
    return create_response("Ok", "Conversation service is healthy.", request.state.txid, 200)

