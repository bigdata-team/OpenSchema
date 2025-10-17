from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    service_id: str
    model_name: str = "gpt-4o"
    question: str
    temperature: str
    top_p: float
    top_k: int
    stream: bool = True
    