from common.model.sql import BaseOrm


class File(BaseOrm):
    file_name: str
    s3_path: str
