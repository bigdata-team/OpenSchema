from common.model.sql import BaseOrm


class History(BaseOrm, table=True):
    user_id: str | None
    service_id: str | None
    url: str | None
    request: str | None
    response: str | None
    completion_id: str | None
    model_name: str | None
    total_tokens: int | None
    is_stream: bool | None
