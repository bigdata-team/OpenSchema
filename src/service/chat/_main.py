import os, json, httpx
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import StreamingResponse
from router import private_router, public_router
from starlette.middleware.cors import CORSMiddleware

from common.config import PROJECT_NAME, SERVICE_VERSION, SERVICE_NAME
from common.connection.kafka import KafkaConnection
from common.connection.sql import PostgresConnection
from common.lifespan import compose
from common.middleware import CorrelationIdMiddleware
from openai import AsyncOpenAI
from model.chat import *

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = (
    "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"
)


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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    server_url = app.root_path
    openapi_schema["servers"] = [{"url": server_url}]
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Use jwt access token for authorization",
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.post("/completions")
async def chat(body: ChatRequest):
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": body.model_name,
        "messages": [
            {"role": "user", "content": body.question},
        ],
        "temperature": body.temperature,
        "top_p": body.top_p,
        "top_k": body.top_k,
        "stream": body.stream,
    }

    if body.stream:

        async def stream_generator(url: str, headers: dict, data: dict):
            buffer = []
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream(
                    "POST", url, headers=headers, json=data
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            b = line.removeprefix("data: ")
                            if not b.strip() == "[DONE]":
                                buffer.append(b)
                            yield line

            buffer = [json.loads(b) for b in buffer]
            buffer = [
                item["choices"][0]["delta"]["content"]
                for item in buffer
                if "choices" in item
            ]
            asnwer_text = "".join(buffer)

        return StreamingResponse(
            stream_generator(url=url, headers=headers, data=data),
            media_type="text/event-stream",
        )
    else:
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
