import io
import json
import os
from io import BytesIO
from pathlib import Path

import httpx
from docx import Document
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from models.mongo import *
from models.prompt import Reference, Topic
from openai import OpenAI
from utils import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_pptx,
    extract_text_from_txt,
)

from common.chat import Handler
from common.lifespan import compose, kafka, mongo, neo4j, postgres
from common.middleware import *
from common.models.event import create_event
from common.models.http import DataResponseModel, create_response
from common.utils import stringify

PROXY_CHAT_BASE_URL = os.getenv("PROXY_CHAT_BASE_URL")
SERVICE_ID = os.getenv("SERVICE_ID")
MONGO_DB = os.getenv("MONGO_DB")


app = FastAPI(
    root_path="/api/v1/knowledgebase",
    lifespan=compose(kafka, mongo, neo4j),
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
    db = app.state.mongo
    db.command("ping")
    async with app.state.neo4j.session() as session:
        await session.run("RETURN 1")
    return create_response("Ok", "Knowledge base ingest service is healthy.", None, 200)


async def preprocess(
    app,
    request,
    tasks,
    job_id,
    user_id,
    file_id,
    file_name,
    file_extension,
    file_content,
):
    await app.state.mongo[MONGO_DB].update_one(
        {"job_id": job_id},
        {
            "$set": {
                "job_status": "running:1/2",
                "user_id": user_id,
                "file_name": file_name,
                "file_extension": file_extension,
            }
        },
    )

    if file_extension == ".pdf":
        content_type = "application/pdf"
        extracted_data = extract_text_from_pdf(file_content)
    elif file_extension == ".docx":
        content_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        extracted_data = extract_text_from_docx(file_content)
    elif file_extension == ".pptx":
        content_type = (
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        extracted_data = extract_text_from_pptx(file_content)
    elif file_extension == ".txt":
        content_type = "plain/text"
        extracted_data = extract_text_from_txt(file_content)
    elif file_extension == ".md":
        content_type = "plain/markdown"
        extracted_data = extract_text_from_txt(file_content)
    else:
        raise Exception("Unsupported file type.")

    pages = [PageObject(**page).model_dump() for page in extracted_data]
    await app.state.mongo[MONGO_DB].update_one(
        {"job_id": job_id},
        {
            "$set": {
                "job_status": "running:2/2",
                "user_id": user_id,
                "file_name": file_name,
                "file_extension": file_extension,
                "content_type": content_type,
                "pages": pages,
            }
        },
    )

    client = OpenAI(base_url=PROXY_CHAT_BASE_URL, api_key=request.state.token_string)
    completion = client.chat.completions.parse(
        model="google/gemini-2.5-flash",
        extra_headers={
            "X-Service-Id": SERVICE_ID,
        },
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert at structured data extraction. You will be given unstructured text from a document and should convert it into the given structure.
                Your task is to process text and extract all meaningful entities, their topics, and their content. You are to return an array of objects with the title being the topic name, and the description being the content of the topic. Be as detailed as possible, and ensure that each topic is distinct and non-overlapping. Do not describe any images, only the text content.
                Output ONLY valid JSON matching the schema provided. Do not include any explanations or extra text.
                """,
            },
            {"role": "user", "content": f"{stringify(pages)}."},
        ],
        response_format=Topic,
    )

    print("**************************")
    print(completion)
    print("**************************")

    await app.state.mongo[MONGO_DB].update_one(
        {"job_id": job_id},
        {
            "$set": {
                "job_status": "done",
            }
        },
    )


@app.post("/upload")
@identify
async def upload(
    request: Request, tasks: BackgroundTasks, file: UploadFile = File(...)
):
    job_id = str(uuid4())
    user_id = request.state.token.sub if request.state.token else None

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
        file_name = file.filename
        file_content = await file.read()

        url = "http://s3-gateway:8000/api/v1/storage/upload"
        headers = {"X-Service-Id": SERVICE_ID}
        files = {"file": (file_name, file_content, file.content_type)}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, files=files)
            response = response.json()
            file_id = response.get("data").get("upload_id")

    except Exception as e:
        return create_response("Error", str(e), None, 500)

    tasks.add_task(
        preprocess,
        app=app,
        request=request,
        tasks=tasks,
        job_id=job_id,
        user_id=user_id,
        file_id=file_id,
        file_name=file_name,
        file_extension=file_extension,
        file_content=file_content,
    )

    fileobject = FileObject(
        id=file_id,
        job_id=job_id,
        job_status="queued",
    )
    await app.state.mongo[MONGO_DB].insert_one(fileobject.model_dump())

    return create_response(
        "Success",
        "File uploaded successfully.",
        {"job_id": job_id},
        200,
    )


@app.get("/jobs/{job_id}")
async def get_job(job_id: str, request: Request):
    result = await app.state.mongo[MONGO_DB].find_one(
        {"job_id": job_id}, {"job_status": 1, "_id": 0}
    )
    job_status = result.get("job_status", "unknown") if result else "unknown"
    return create_response("Ok", "Job status.", {"status": job_status}, 200)
