import json
import os
from pathlib import Path
from uuid import uuid4

import httpx
from celery import chain, signature
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from models.http import *
from models.mongo import *
from models.prompt import Topics
from openai import AsyncOpenAI
from utils import (
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_pptx,
    extract_text_from_txt,
)

from common.connection.celery import get_client
from common.lifespan import compose, kafka, mongo, neo4j, postgres
from common.middleware import *
from common.models.http import DataResponseModel, create_response
from common.connection.util.util import stringify

SERVICE_ID = os.getenv("SERVICE_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME")

PROXY_CHAT_BASE_URL = os.getenv("PROXY_CHAT_BASE_URL")
PROXY_EMBEDDINGS_BASE_URL = os.getenv("PROXY_EMBEDDINGS_BASE_URL")

MONGO_DB = os.getenv("MONGO_DB")
VECTOR_DIMENSIONS = os.getenv("VECTOR_DIMENSIONS")


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
                "file_id": file_id,
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
                "file_id": file_id,
                "file_name": file_name,
                "file_extension": file_extension,
                "content_type": content_type,
                "pages": pages,
            }
        },
    )

    client = AsyncOpenAI(
        base_url=PROXY_CHAT_BASE_URL, api_key=request.state.token_string
    )
    completion = await client.chat.completions.parse(
        extra_headers={
            "X-Service-Id": SERVICE_ID,
        },
        model="google/gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert at structured data extraction. You will be given unstructured text from a document and should convert it into the given structure.
                Your task is to process text and extract all meaningful entities, their topics, and their content. Be as detailed as possible, and ensure that each topic is distinct and non-overlapping.
                Do not describe any images, only the text content.
                """,
            },
            {"role": "user", "content": f"{stringify(pages)}."},
        ],
        response_format=Topics,
    )

    await app.state.mongo[MONGO_DB].update_one(
        {"job_id": job_id},
        {
            "$set": {
                "job_status": "topics created",
            }
        },
    )

    data = json.loads(completion.choices[0].message.content)
    text_batch = [
        topic.get("title") + "\n\n" + topic.get("explanation")
        for topic in data.get("topics")
    ]

    async with app.state.neo4j.session() as kg:
        await kg.run(
            """
        CREATE CONSTRAINT unique_topic IF NOT EXISTS
            FOR (t:Topic) REQUIRE t.topicId IS UNIQUE
        """
        )

        await kg.run(
            """
        CREATE VECTOR INDEX `vindex` IF NOT EXISTS
            FOR (t:Topic) ON (t.textEmbedding)
            OPTIONS { indexConfig: {
                `vector.dimensions`: $vector_dimensions,
                `vector.similarity_function`: 'cosine'
            }}
        """,
            params={"vector_dimensions": os.getenv("VECTOR_DIMENSIONS")},
        )

    client = AsyncOpenAI(
        base_url=PROXY_EMBEDDINGS_BASE_URL, api_key=request.state.token_string
    )
    embedding_response = await client.embeddings.create(
        extra_headers={
            "X-Service-Id": SERVICE_ID,
        },
        input=text_batch,
        model="text-embedding-3-small",
    )
    embedded_vectors = embedding_response.data[0].embedding

    await app.state.mongo[MONGO_DB].update_one(
        {"job_id": job_id},
        {
            "$set": {
                "job_status": "embedded",
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
            response.raise_for_status()  # Raise an exception for HTTP error responses
            response = response.json()
            file_id = response.get("data").get("id")

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
        file_id=file_id,
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


@app.get("/upload/jobs/{job_id}")
async def upload_job(job_id: str, request: Request):
    result = await app.state.mongo[MONGO_DB].find_one(
        {"job_id": job_id}, {"job_status": 1, "_id": 0}
    )
    job_status = result.get("job_status", "unknown") if result else "unknown"
    return create_response("Ok", "Job status.", {"status": job_status}, 200)


@app.post("/vindex")
@identify
async def vindex(request: Request, body: JobIdModel, tasks: BackgroundTasks):
    return create_response("Ok")


@app.post("/waterfall")
@identify
async def waterfall(request: Request, file: UploadFile = File(...)):
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
            file_id = response.get("data").get("id")
            file_path = response.get("data").get("file_path")

    except Exception as e:
        return create_response("Error", str(e), None, 500)

    job_id = str(uuid4())

    client = get_client("clientA")
    print(client)

    payload = {"job_id": job_id, "file_id": file_id, "file_path": file_path}

    from common.jobs import process

    # Create a Celery job for processing
    wf = chain(
        process.s(payload).set(queue="q_default"),
    )

    on_err = signature("app.tasks.pipeline.cleanup", immutable=True).set(
        queue="q_default"
    )

    result = wf.apply_async(link_error=[on_err], headers={"job_id": job_id})

    return create_response(
        "Success",
        "Job created successfully.",
        {"job_id": job_id, "task_id": result.id},
        200,
    )
