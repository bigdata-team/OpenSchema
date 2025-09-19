from fastapi.responses import StreamingResponse, Response
import json
import httpx

async def proxy(
    url, method, headers, body
):
    async def stream_generator():
        chunks = ""
        async with httpx.AsyncClient(timeout=600) as client:
            async with client.stream(
                method, url, headers=headers, content=body
            ) as res:
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
        chunks = [ c.get("choices")[0].get("delta").get("content") for c in chunks ]
        chunks_as_text = "".join(chunks)
        #NOTE add dbworks

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

            chunks = json.loads(content)
            chunks_as_objects = chunks
            chunks_as_text = chunks.get("choices")[0].get("message").get("content")
            #NOTE add dbworks

        return Response(
            content=content,
            status_code=status,
            media_type=content_type
        )
    