from fastapi import FastAPI

from common.lifespan import compose, init_schema, kafka, postgres
from common.models.http import create_response, DataResponseModel
from common.models.event import create_event
from common.middleware import TransactionIDMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from sqlalchemy import text
from models.http import *
from models.db import *
from common.connection.postgres import engine
from common.jwt import JWTManager
from fastapi import Depends
from fastapi.responses import StreamingResponse, Response
from common.jwt import get_tokens
import httpx
import os

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

jwt = JWTManager()

app = FastAPI(
    root_path="/api/v1/proxy",
    lifespan=compose(init_schema(engine), kafka, postgres),
)
app.add_middleware(TransactionIDMiddleware)
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
        "Ok", "Proxy service is healthy.", request.state.txid, 200
    )


# /chat/completions
@app.post("/{path:path}")
async def proxy(path: str, request: Request, tokens=Depends(get_tokens)):
    token = tokens.get("access_token") or tokens.get("bearer_token") or None
    payload = await jwt.verify_token(token, "auth.service", "service")

    url = f"{OPENROUTER_BASE_URL}/{path}"
    method = "POST"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    body = await request.body()

    async def stream_generator():
        async with httpx.AsyncClient(timeout=600) as client:
            async with client.stream(
                method, url, headers=headers, content=body
            ) as res:
                async for chunk in res.aiter_bytes():
                    yield chunk

    async with httpx.AsyncClient(timeout=600) as client:
        async with client.stream(
            method, url, headers=headers, content=body
        ) as res:
            content_type = res.headers.get("content-type", "")
            status = res.status_code

            content = await res.aread()

    if content_type.startswith("text/event-stream"):
        return StreamingResponse(
            stream_generator(),
            status_code=status,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    else:
        async with httpx.AsyncClient(timeout=600) as client:
            async with client.stream(
                method, url, headers=headers, content=body
            ) as res:
                content = await res.aread()
        return Response(
            content=content,
            status_code=status,
            media_type=content_type,
        )


@app.get("/list")
async def list_conversations(
    tokens: dict = Depends(get_tokens),
):
    token = tokens.get("access_token") or tokens.get("bearer_token") or None
    payload = await jwt.verify_token(token, "auth.service", "service")

    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        conversations = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == payload.sub)
            .order_by(Conversation.created_at.desc())
        )
        conversations = conversations.scalars().all()

    return create_response(
        "Ok",
        "Conversations list retrieved successfully.",
        [c.to_dict() for c in conversations],
        200,
    )


@app.get("/list/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    tokens: dict = Depends(get_tokens),
):
    token = tokens.get("access_token") or tokens.get("bearer_token") or None
    payload = await jwt.verify_token(token, "auth.service", "service")

    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        conversation = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == payload.sub,
            )
        ).scalar_one_or_none()

    if not conversation:
        return create_response(
            "Not found", "Conversation not found.", None, 404
        )

    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        messages = (
            await db.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.asc())
            )
            .scalars()
            .all()
        )

    return create_response(
        "Ok",
        "Conversation retrieved successfully.",
        {"conversation": conversation, "messages": messages},
        200,
    )
