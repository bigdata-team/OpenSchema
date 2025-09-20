import json

import httpx
from fastapi import BackgroundTasks, FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, StreamingResponse


class Handler:
    def __init__(
        self,
        url: str,
        headers: dict,
        body: bytes,
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

    def stream_parser(self, content: str) -> list[any]:
        chunks = []
        for chunk in content.split("\n\n"):
            if chunk.startswith("data: "):
                chunk = chunk.removeprefix("data: ").strip()
                if chunk != "[DONE]":
                    chunks.append(json.loads(chunk))
        return chunks

    def nonstream_parser(self, content: any) -> any:
        if isinstance(content, (bytes, bytearray)):
            content = content.decode("utf-8")
        return json.loads(content)

    async def __call__(self):
        client = httpx.AsyncClient(timeout=600)
        returned_streaming = False
        req = client.build_request(
            "POST",
            self.url,
            headers=self.headers,
            content=self.body,
        )
        res = await client.send(req, stream=True)

        try:
            content_type = res.headers.get("content-type", "")
            status = res.status_code

            if content_type.startswith("text/event-stream"):

                async def stream_generator():
                    temp = ""
                    try:
                        async for b in res.aiter_bytes():
                            chunk = b.decode("utf-8", errors="ignore")
                            temp += chunk
                            yield b
                    finally:
                        # Schedule storing after stream completes
                        self.tasks.add_task(self.stream_parser, content=temp)
                        try:
                            await res.aclose()
                        finally:
                            await client.aclose()

                returned_streaming = True
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
            else:
                content = await res.aread()
                try:
                    self.tasks.add_task(self.nonstream_parser, content=content)
                    return Response(
                        content=content,
                        status_code=status,
                        media_type=content_type,
                    )
                finally:
                    await res.aclose()
                    await client.aclose()
        finally:
            # If we didn't return a StreamingResponse, ensure cleanup here
            if not returned_streaming:
                try:
                    if not res.is_closed:
                        await res.aclose()
                finally:
                    if not client.is_closed:
                        await client.aclose()

    async def run(self):
        return await self.__call__()
