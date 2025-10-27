from pydantic import BaseModel
from model.sql.chat import Chat


class Message(BaseModel):
    role: str = "user"
    content: str = "한국 수도"


class ChatRequest(BaseModel):
    parent_id : str
    model: str = "openai/gpt-5"
    messages: list[Message]
    stream: bool = True
    system_prompt: str | None = None
    temperature: float = 0.7
    top_p: float = 1.0
    top_k: int = 50

class ChatTitleRequest(BaseModel):
    id : str | None
    title : str

class ChatCreateRequest(BaseModel):
    parent_id: str

class ChatListRequest(BaseModel):
    id : str 


class ChatChild(BaseModel):
    id: str
    #
    parent_id: str | None
    title: str | None
    #
    user_id: str | None
    service_id: str | None
    url: str | None
    user_prompt: str | None
    answer: str | None
    request: str | None
    response: str | None
    #
    completion_id: str | None
    model_name: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    is_stream: bool | None
    system_prompt: str | None
    parameters: str | None
    #
    children: list[Chat]

class ChatResponse(BaseModel):
    id: str
    #
    parent_id: str | None
    title: str | None
    #
    user_id: str | None
    service_id: str | None
    url: str | None
    user_prompt: str | None
    answer: str | None
    request: str | None
    response: str | None
    #
    completion_id: str | None
    model_name: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    is_stream: bool | None
    system_prompt: str | None
    parameters: str | None
    #
    children: list[ChatChild]

