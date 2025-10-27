from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks

from common.middleware.authorization import get_auth_dependency
from common.model.http import create_response
from model.http.chat import ChatRequest
from service.chat import ChatService

from common.model.http import create_response

router = APIRouter(tags=["public"]) # TODO , prefix="/public")


@router.get("/ping")
async def ping():
    return create_response(detail="pong")

""" TODO
@router.post("/completions")
async def completions(req_body: ChatRequest, tasks: BackgroundTasks, service: ChatService = Depends(ChatService)):
    print(f"TODO >>> completions: {req_body}")
    return await service.chat(req_body=req_body, tasks=tasks)
"""