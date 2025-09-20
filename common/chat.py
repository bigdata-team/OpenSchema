import json

import httpx
from fastapi import BackgroundTasks, FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse


class Handler:
    """Thin HTTP proxy handler with clear streaming vs non‑streaming paths.

    Key points:
    - No nested try/finally ladders; resource lifetimes are obvious.
    - Uses a single client+response lifecycle per request.
    - Schedules parsing work via BackgroundTasks after body/stream finishes.
    """

    def __init__(
        self,
        url: str,
        headers: dict,
        body: dict,
        app: FastAPI,
        request: Request,
        tasks: BackgroundTasks,
    ):
        self.url = url
        self.headers = headers
        self.body = body
        self.app = app
        self.request = request
        self.tasks = tasks

    def stream_parser(self, content: str) -> any:
        chunks = []
        for chunk in content.split("\n\n"):
            if chunk.startswith("data: "):
                chunk = chunk.removeprefix("data: ").strip()
                if chunk != "[DONE]":
                    chunks.append(json.loads(chunk))
        return chunks

    def nonstream_parser(self, content: str) -> any:
        return json.loads(content)

    async def __call__(self):
        client = httpx.AsyncClient(timeout=600)
        req = client.build_request(
            "POST",
            self.url,
            headers=self.headers,
            json=self.body,
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
                    self.tasks.add_task(self.stream_parser, content=accumulated_text)
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
        self.tasks.add_task(self.nonstream_parser, content=content.decode("utf-8"))
        response = Response(
            content=content,
            status_code=status,
            media_type=content_type or "application/json",
        )
        await res.aclose()
        await client.aclose()
        return response

    async def run(self):
        return await self.__call__()
