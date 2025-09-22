import json
import os
from pathlib import Path

import httpx
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from models.db import *
from models.http import *
from sqlalchemy import text

from common.chat import Handler
from common.lifespan import compose, kafka, postgres, s3
from common.middleware import *
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response
from common.utils import Now

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "default")
S3_PRESIGN_EXPIRE_SECONDS = int(os.getenv("S3_PRESIGN_EXPIRE_SECONDS", 900))

app = FastAPI(
    root_path="/api/v1/storage",
    lifespan=compose(kafka, postgres, s3),
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


@app.post("/upload")
@identify
async def upload(request: Request, file: UploadFile = File(...)):
    if file is None:
        return create_response("Error", "No file uploaded.", None, 400)

    service_id = request.headers.get("X-Service-Id") or "anon"
    file_name = file.filename
    file_extension = Path(file_name).suffix

    file_uuid = str(uuid4())
    now = Now().now
    yyyy, mm, dd = f"{now.year:0>4}", f"{now.month:0>2}", f"{now.day:0>2}"

    file_path = f"uploads/{service_id}/{yyyy}/{mm}/{dd}/{file_uuid}{file_extension}"

    async with app.state.s3 as s3:
        await s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_path,
            Body=await file.read(),
            ContentType=file.content_type or "application/octet-stream",
        )

    async with app.state.postgres_session() as db:
        upload = Upload(
            id=file_uuid,
            user_id=(request.state.token.sub if request.state.token else None),
            service_id=service_id,
            file_name=file_name,
            file_path=file_path,
            is_uploaded=True,
        )
        db.add(upload)
        await db.commit()
        upload_id = upload.id

    return create_response(
        "Ok",
        "File uploaded successfully.",
        UploadIdModel(upload_id=upload_id),
        200,
    )


@app.post("/upload/presign", response_model=DataResponseModel[UploadResultModel])
@identify
async def upload_presign(request: Request, body: UploadModel):
    """
    Example:
        curl -X PUT "<PRESIGNED_URL>" \
            -H "Content-Type: application/octet-stream" \
            --data-binary "@path/to/your/file"
    """
    service_id = body.service_id or request.headers.get("X-Service-Id") or "anon"
    file_name = body.file_name
    file_extension = Path(file_name).suffix

    file_uuid = body.upload_id or str(uuid4())
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
        presigned_url = presigned_url.replace("http://s3:9000", "http://localhost:9000")

    async with app.state.postgres_session() as db:
        upload = Upload(
            id=file_uuid,
            user_id=request.state.token.sub if request.state.token else None,
            service_id=service_id,
            file_name=file_name,
            file_path=file_path,
        )
        db.add(upload)
        await db.commit()

        upload_id = upload.id

    return create_response(
        "Ok",
        "Presigned URL generated.",
        UploadResultModel(url=presigned_url, upload_id=upload_id),
        200,
    )


@app.post("/upload/completed")
async def upload_completed(request: Request, body: UploadIdModel):
    upload_id = body.upload_id
    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        upload = await db.execute(select(Upload).where(Upload.id == upload_id))
        upload = upload.scalar_one_or_none()
        upload.is_uploaded = True
        await db.commit()
        await db.refresh(upload)

    service_id = upload.service_id
    service_id = service_id.removesuffix(".service")
    await app.state.kafka_producer.send_and_wait(
        topic=f"{service_id}.uploaded",
        value=create_event(cid=request.state.cid),
    )
    return create_response("Ok", f"Message created for {service_id}.", None, 200)


@app.post("/download")
async def download(request: Request, body: UploadIdModel):
    upload_id = body.upload_id
    if not upload_id:
        return create_response("Error", "Missing upload_id.", None, 400)

    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        upload = await db.execute(select(Upload).where(Upload.id == upload_id))
        upload = upload.scalar_one_or_none()
        if not upload or not upload.is_uploaded:
            return create_response(
                "Error", "File not found or not uploaded.", None, 404
            )
        file_path = upload.file_path
        file_name = upload.file_name

    async with app.state.s3 as s3:
        try:
            obj = await s3.get_object(Bucket=S3_BUCKET_NAME, Key=file_path)
            content = await obj["Body"].read()
            content_type = obj.get("ContentType", "application/octet-stream")
        except Exception as e:
            return create_response("Error", f"Failed to download file: {e}", None, 500)

    headers = {"Content-Disposition": f'attachment; filename="{file_name}"'}
    return Response(content, media_type=content_type, headers=headers)


@app.post("/download/presign")
async def download_presign(request: Request, body: UploadIdModel):
    upload_id = body.upload_id
    if not upload_id:
        return create_response("Error", "Missing upload_id.", None, 400)

    async with app.state.postgres_session() as db:
        from sqlalchemy.future import select

        upload = await db.execute(select(Upload).where(Upload.id == upload_id))
        upload = upload.scalar_one_or_none()
        if not upload or not upload.is_uploaded:
            return create_response(
                "Error", "File not found or not uploaded.", None, 404
            )
        file_path = upload.file_path

    async with app.state.s3 as s3:
        try:
            presigned_url = await s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": S3_BUCKET_NAME,
                    "Key": file_path,
                },
                ExpiresIn=S3_PRESIGN_EXPIRE_SECONDS,
            )
            presigned_url = presigned_url.replace(
                "http://s3:9000", "http://localhost:9000"
            )
        except Exception as e:
            return create_response(
                "Error", f"Failed to generate presigned URL: {e}", None, 500
            )

    return create_response(
        "Ok",
        "Presigned URL generated.",
        {"url": presigned_url, "upload_id": upload_id},
        200,
    )
