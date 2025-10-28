from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks

from common.middleware.authorization import get_auth_dependency
from common.model.http import create_response
from model.http.chat import ChatCompletionRequest, ChatTitleCreateRequest, ChatTitleUpdateRequest, ChatTitleDeleteRequest, ChatCreateRequest, ChatListRequest
from service.chat import ChatService

router = APIRouter(
    tags=["private"],
    dependencies=[
        Depends(
            get_auth_dependency(
                auth_header="Authorization",
                token_prefix="Bearer ",
                issuer="auth.service",
                audience="service",
            )
        ),
    ],
)


@router.get("/_ping")
async def ping():
    return create_response(detail="pong")

""" TODO
@router.get("/chat")
async def chat():
    print(f"TODO >>> chat")
    return create_response(detail="chat")
"""

####################################################################################################
@router.post("/title")
async def create_chat_title(req_body: ChatTitleCreateRequest, service: ChatService = Depends(ChatService)):
    print(f"TODO >>> title create: {req_body}")
    data = await service.create_chat_title(title=req_body.title)
    return create_response(data=data)

@router.patch("/title")
async def update_chat_title(req_body: ChatTitleUpdateRequest, service: ChatService = Depends(ChatService)):
    print(f"TODO >>> title update: {req_body}")
    data = await service.update_chat_title(id=req_body.id, title=req_body.title)
    return create_response(data=data)

@router.delete("/title")
async def delete_chat_title(req_body: ChatTitleDeleteRequest, service: ChatService = Depends(ChatService)):
    print(f"TODO >>> title delete: {req_body}")
    data = await service.delete_chat_title(id=req_body.id)
    return create_response(data=data)

@router.get("/title")
async def list_chat_title(service: ChatService = Depends(ChatService)):
    print(f"TODO >>> title list")
    data = await service.list_chat_title()
    return create_response(data=data)


####################################################################################################
@router.post("/")
async def create_chat(req_body: ChatCreateRequest,service: ChatService = Depends(ChatService)):
    print(f"TODO >>> chat create")
    data = await service.create_chat(parent_id = req_body.parent_id)
    return create_response(data=data)

@router.get("/")
async def get_chat_with_children(params: ChatListRequest = Depends(),service: ChatService = Depends(ChatService)):
    print(f"TODO >>> chat get")
    data = await service.get_chat_with_children(id = params.id)
    return create_response(data=data)



####################################################################################################
@router.post("/completions")
async def completions(req_body: ChatCompletionRequest, tasks: BackgroundTasks, service: ChatService = Depends(ChatService)):
    print(f"TODO >>> completions: {req_body}")
    return await service.completions(req_body=req_body, tasks=tasks)

@router.post("/conversations")
async def conversations(req_body: ChatCompletionRequest, tasks: BackgroundTasks, service: ChatService = Depends(ChatService)):
    print(f"TODO >>> conversations: {req_body}")
    if not req_body.parent_id or req_body.parent_id.strip() == "" or req_body.parent_id == "string":
        return create_response(code=400, detail="parent_id is required")
    return await service.conversations(req_body=req_body, tasks=tasks)