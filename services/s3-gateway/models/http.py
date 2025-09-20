from pydantic import BaseModel


class UploadModel(BaseModel):
    service_id: str = None
    file_name: str = None
    file_extension: str = None
    upload_id: str = None


class UploadResultModel(BaseModel):
    url: str
    upload_id: str


class CompletedModel(BaseModel):
    upload_id: str
