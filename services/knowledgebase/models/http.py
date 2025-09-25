from pydantic import BaseModel


class JobIdModel(BaseModel):
    job_id: str
