from pydantic import BaseModel


class UploadModel(BaseModel):
    upload_id: str = None
    service_id: str = None
    file_name: str = None


class UploadResultModel(BaseModel):
    upload_id: str
    url: str


class UploadIdModel(BaseModel):
    upload_id: str
