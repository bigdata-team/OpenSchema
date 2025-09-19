from fastapi.responses import StreamingResponse, Response
import json
import httpx
from fastapi.requests import Request
from fastapi import BackgroundTasks
from fastapi import FastAPI


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
        async with httpx.AsyncClient(timeout=600) as client:
            async with client.stream(
                "POST",
                self.url,
                headers=self.headers,
                content=self.body,
            ) as res:
                content_type = res.headers.get("content-type", "")
                status = res.status_code

                if content_type.startswith("text/event-stream"):

                    async def stream_generator():
                        temp = ""
                        async for b in res.aiter_bytes():
                            try:
                                temp += b.decode("utf-8")
                            except Exception:
                                temp += b.decode("utf-8", errors="ignore")
                            yield b
                        self.tasks.add_task(self.stream_parser, content=temp)

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
                    content = await res.aread()
                    self.tasks.add_task(self.nonstream_parser, content=content)
                    return Response(
                        content=content, status_code=status, media_type=content_type
                    )

    async def run(self):
        return await self.__call__()
