import json
import os

import httpx
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from models.db import *
from models.http import *
from sqlalchemy import text

from common.chat import Handler
from common.connection.postgres import engine
from common.lifespan import compose, init_schema, kafka, postgres, s3
from common.middleware import *
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response
from common.utils import Now

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "default")
S3_PRESIGN_EXPIRE_SECONDS = int(os.getenv("S3_PRESIGN_EXPIRE_SECONDS", 900))

app = FastAPI(
    root_path="/api/v1/storage",
    lifespan=compose(init_schema(engine), kafka, postgres, s3),
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
    async with app.state.s3 as s3:
        try:
            await s3.list_buckets()
        except Exception as e:
            return create_response("Error", str(e), None, 500)
    return create_response("Ok", "Storage gateway service is healthy.", None, 200)


@app.post("/upload/presign")
@identify
async def upload_presign(request: Request, body: UploadModel):
    """
    Example:
        curl -X PUT "<PRESIGNED_URL>" \
            -H "Content-Type: application/octet-stream" \
            --data-binary "@path/to/your/file"
    """
    service_id = body.service_id or "anon"
    file_name = body.file_name
    file_extension = body.file_extension
    if file_extension and not file_extension.startswith("."):
        file_extension = "." + file_extension

    file_uuid = str(uuid4())
    now = Now().now
    yyyy, mm, dd = f"{now.year:0>4}", f"{now.month:0>2}", f"{now.day:0>2}"

    file_path = f"uploads/{service_id}/{yyyy}/{mm}/{dd}/{file_uuid}{file_extension}"

    async with app.state.s3 as s3:
        presigned_url = await s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": S3_BUCKET_NAME,
                "Key": file_path,
                "ContentType": "application/octet-stream",
            },
            ExpiresIn=S3_PRESIGN_EXPIRE_SECONDS,
        )
        presigned_url = presigned_url.replace(
            "http://s3-gateway:9000", "http://localhost:9000"
        )

    async with app.state.postgres_session() as db:
        upload = Upload(
            user_id=request.state.token.sub if request.state.token else None,
            service_id=service_id,
            file_name=file_name,
            file_extension=file_extension,
            file_path=file_path,
        )
        db.add(upload)
        await db.commit()

    return create_response(
        "Ok", "Presigned URL generated.", {"url": presigned_url}, 200
    )

