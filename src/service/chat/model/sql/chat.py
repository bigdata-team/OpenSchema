# from sqlmodel import Field

from common.model.sql import BaseOrm


class Chat(BaseOrm, table=True):
    parent_id: str | None
    title: str | None
    index: int | None
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
    # TODO
    # children: list["Chat"] = Field(default_factory=list, exclude=True)