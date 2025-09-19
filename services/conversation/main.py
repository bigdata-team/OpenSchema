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
from fastapi.responses import StreamingResponse, Response
import httpx
import json
import os

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI(
    root_path="/api/v1/conversation",
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
    return create_response("Ok", "Proxy service is healthy.", request.state.txid, 200)


@app.post("")
# @identify
async def chat_proxy(request: Request):
    url = f"http://chat:8000/api/v1/chat/completions"
    method = "POST"
    headers = request.headers
    body = await request.body()

    async def stream_generator():
        chunks = ""
        async with httpx.AsyncClient(timeout=600) as client:
            async with client.stream(method, url, headers=headers, content=body) as res:
                async for b in res.aiter_bytes():
                    chunks += b.decode("utf-8")
                    yield b

        chunks = [
            c.removeprefix("data: ").strip()
            for c in chunks.split("\n\n")
            if c.startswith("data: ")
        ]
        chunks = [json.loads(c) for c in chunks if c and c != "[DONE]"]
        chunks_as_objects = chunks
        chunks = [c.get("choices")[0].get("delta").get("content") for c in chunks]
        chunks_as_text = "".join(chunks)

        # async with app.state.postgres_session() as db:
        #     history = History(
        #         user_id=request.state.payload.sub,
        #         service_name=request.headers.get("X-Service-Name"),
        #         request=json.dumps(json.loads(body)),
        #         response=json.dumps(chunks_as_objects),
        #         tokens=chunks_as_objects[-1].get("usage").get("total_tokens"),
        #     )
        #     db.add(history)
        #     await db.commit()

    async with httpx.AsyncClient(timeout=600) as client:
        async with client.stream(method, url, headers=headers, content=body) as res:
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
            async with client.stream(method, url, headers=headers, content=body) as res:
                content = await res.aread()

            chunks = json.loads(content)
            chunks_as_objects = chunks
            chunks_as_text = chunks.get("choices")[0].get("message").get("content")

            # async with app.state.postgres_session() as db:
            #     history = History(
            #         user_id=request.state.token.sub,
            #         service_name=request.headers.get("X-Service-Name"),
            #         request=json.dumps(json.loads(body)),
            #         response=json.dumps(chunks_as_objects),
            #         tokens=chunks_as_objects.get("usage").get("total_tokens"),
            #     )
            #     db.add(history)
            #     await db.commit()

        return Response(content=content, status_code=status, media_type=content_type)


# @app.get("/list")
# async def list_conversations(
#     tokens: dict = Depends(get_tokens),
# ):
#     token = tokens.get("access_token") or tokens.get("bearer_token") or None
#     payload = await jwt.verify_token(token, "auth.service", "service")

#     async with app.state.postgres_session() as db:
#         from sqlalchemy.future import select

#         conversations = await db.execute(
#             select(Conversation)
#             .where(Conversation.user_id == payload.sub)
#             .order_by(Conversation.created_at.desc())
#         )
#         conversations = conversations.scalars().all()

#     return create_response(
#         "Ok",
#         "Conversations list retrieved successfully.",
#         [c.to_dict() for c in conversations],
#         200,
#     )


# @app.get("/list/{conversation_id}")
# async def get_conversation(
#     conversation_id: str,
#     tokens: dict = Depends(get_tokens),
# ):
#     token = tokens.get("access_token") or tokens.get("bearer_token") or None
#     payload = await jwt.verify_token(token, "auth.service", "service")

#     async with app.state.postgres_session() as db:
#         from sqlalchemy.future import select

#         conversation = await db.execute(
#             select(Conversation).where(
#                 Conversation.id == conversation_id,
#                 Conversation.user_id == payload.sub,
#             )
#         ).scalar_one_or_none()

#     if not conversation:
#         return create_response(
#             "Not found", "Conversation not found.", None, 404
#         )

#     async with app.state.postgres_session() as db:
#         from sqlalchemy.future import select

#         messages = (
#             await db.execute(
#                 select(Message)
#                 .where(Message.conversation_id == conversation_id)
#                 .order_by(Message.created_at.asc())
#             )
#             .scalars()
#             .all()
#         )

#     return create_response(
#         "Ok",
#         "Conversation retrieved successfully.",
#         {"conversation": conversation, "messages": messages},
#         200,
#     )
