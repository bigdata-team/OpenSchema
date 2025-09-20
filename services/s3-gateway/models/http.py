from pydantic import BaseModel


class UploadModel(BaseModel):
    service_id: str = None
    file_name: str = None
    file_extension: str = None
