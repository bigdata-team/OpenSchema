import json
import os
import io
from io import BytesIO

import httpx
from docx import Document
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pathlib import Path
from common.models.http import create_response
from utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_pptx,
    extract_text_from_txt,
)

from common.chat import Handler
from common.connection.postgres import engine
from common.lifespan import compose, init_schema, kafka, postgres, mongo
from common.middleware import *
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response
from common.utils import Now
import os

SERVICE_ID = os.getenv("SERVICE_ID")


app = FastAPI(
    root_path="/api/v1/knowledgebase",
    lifespan=compose(init_schema(engine), kafka, postgres, mongo),
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
    async with app.state.mongo as db:
        await db.command("ping")
    async with app.state.neo4j.session() as session:
        await session.run("RETURN 1")
    return create_response("Ok", "Knowledge base ingest service is healthy.", None, 200)


@app.post("/upload")
# @protected
async def upload(request: Request, file: UploadFile = File(...)):
    if file is None:
        return create_response("Error", "No file uploaded.", None, 400)

    file_extension = Path(file.filename).suffix
    if file_extension not in [".pdf", ".docx", ".pptx", ".hwp", ".txt", ".md"]:
        return create_response(
            "Error",
            "Unsupported file type. Only PDF, Word, PowerPoint, HWP, TXT, and Markdown files are supported.",
            None,
            400,
        )

    try:
        file_content = await file.read()

        url = "http://s3-gateway:8000/api/v1/storage/upload"
        headers = {"X-Service-Id": SERVICE_ID}
        files = {"file": (file.filename, file_content, file.content_type)}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, files=files)

        if file_extension == ".pdf":
            extracted_text = extract_text_from_pdf(file_content)
        elif file_extension == ".docx":
            extracted_text = extract_text_from_docx(file_content)
        elif file_extension == ".pptx":
            extracted_text = extract_text_from_pptx(file_content)
        elif file_extension in [".txt", ".md"]:
            extracted_text = extract_text_from_txt(file_content)
        else:
            return create_response("Error", "Unsupported file type.", None, 400)

        data = {
            "file_name": file.filename,
            "file_extension": file_extension,
            "data": extracted_text,  # [{ page: int, content: str }]
        }

    except Exception as e:
        return create_response("Error", str(e), None, 500)

    return create_response(
        "Success",
        "File processed and uploaded successfully.",
        data,
        200,
    )
