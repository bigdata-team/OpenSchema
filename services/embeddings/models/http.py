from pydantic import BaseModel


class MessageModel(BaseModel):
    role: str
    content: str


class ConversationModel(BaseModel):
    conversation_id: str
    messages: list[MessageModel]
    timezone: str = "UTC"
