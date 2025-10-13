from typing import Any, TypeVar

from aioboto3 import Session
from fastapi import Depends

from common.lifespan.s3 import get_s3_session
from common.repository import Repository

T = TypeVar("T")


class S3Repository(Repository[Any]):
    def __init__(self, s3):
        super().__init__(Any)
        self.s3: Session = s3.get("client")
        self.bucket_name: str = s3.get("bucket_name")

    async def connect(self) -> None:
        await self.s3.list_buckets()

    async def create_or_update(self, id: str, obj: Any) -> Any:
        await self.s3.put_object(Bucket=self.bucket_name, Key=id, Body=obj)
        return obj

    async def get(self, id: str) -> Any | None:
        response = await self.s3.get_object(Bucket=self.bucket_name, Key=id)
        body = await response["Body"].read()
        return body

    async def delete(self, id: str) -> None:
        await self.s3.delete_object(Bucket=self.bucket_name, Key=id)


def create_s3_repo() -> callable:
    async def _get_repo(s3=Depends(get_s3_session())) -> S3Repository:
        return S3Repository(s3)

    return _get_repo
