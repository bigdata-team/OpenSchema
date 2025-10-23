import os
import json, httpx
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from router import private_router, public_router
from starlette.middleware.cors import CORSMiddleware

from common.config import PROJECT_NAME, SERVICE_VERSION, SERVICE_NAME
from common.connection.kafka import KafkaConnection
from common.connection.sql import PostgresConnection
from common.util.lifespan import compose
from common.middleware import CorrelationIdMiddleware
from model.sql.history import History
from common.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL

pg = PostgresConnection()
kafka = KafkaConnection()

lifespan = compose(PostgresConnection, KafkaConnection)

app = FastAPI(
    title=PROJECT_NAME,
    version=SERVICE_VERSION,
    root_path=f"/api/{SERVICE_VERSION}/{SERVICE_NAME}",
    lifespan=lifespan,
)

app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router, prefix="")
app.include_router(private_router, prefix="")


from fastapi import Request, BackgroundTasks
from fastapi.responses import Response, StreamingResponse
import json


def stream_parser(content: str) -> list:
    chunks = []
    for chunk in content.split("\n\n"):
        if chunk.startswith("data: "):
            chunk = chunk.removeprefix("data: ").strip()
            if chunk != "[DONE]":
                chunks.append(json.loads(chunk))
    return chunks


def nonstream_parser(content: str) -> dict:
    return json.loads(content)


@app.post("/completions")
async def chat_proxy(request: Request, tasks: BackgroundTasks):
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    body = await request.json()

    client = httpx.AsyncClient(timeout=600)
    req = client.build_request(
        "POST",
        url,
        headers=headers,
        json=body,
    )
    res = await client.send(req, stream=True)

    content_type = res.headers.get("content-type", "")
    status = res.status_code

    if content_type.startswith("text/event-stream"):

        async def stream_generator():
            accumulated_text = ""
            try:
                async for b in res.aiter_bytes():
                    accumulated_text += b.decode("utf-8", errors="ignore")
                    yield b
            finally:
                tasks.add_task(stream_parser, content=accumulated_text)
                await res.aclose()
                await client.aclose()

        return StreamingResponse(
            stream_generator(),
            status_code=status,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )

    content = await res.aread()
    tasks.add_task(nonstream_parser, content=content.decode("utf-8"))
    response = Response(
        content=content,
        status_code=status,
        media_type=content_type or "application/json",
    )
    await res.aclose()
    await client.aclose()
    return response
