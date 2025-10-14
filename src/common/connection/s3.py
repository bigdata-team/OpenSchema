from common.config import (
    S3_ACCESS_KEY,
    S3_BUCKET_NAME,
    S3_ENDPOINT,
    S3_REGION_NAME,
    S3_SECRET_KEY,
)

from .connection import ConnectionBase


class S3ConnectionBase(ConnectionBase):
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        region_name: str,
        bucket_name: str,
    ):
        import aioboto3
        from botocore.config import Config

        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name
        self.config = Config(s3={"addressing_style": "path"})
        self.bucket_name = bucket_name

        self.session = aioboto3.Session()

    async def create_bucket(self):
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
            config=self.config,
        ) as client:
            existing_buckets = await client.list_buckets()
            bucket_names = [
                bucket["Name"] for bucket in existing_buckets.get("Buckets", [])
            ]

            if self.bucket_name not in bucket_names:
                create_kwargs = {"Bucket": self.bucket_name}
                if self.region_name and self.region_name != "us-east-1":
                    create_kwargs["CreateBucketConfiguration"] = {
                        "LocationConstraint": self.region_name
                    }
                await client.create_bucket(**create_kwargs)

    async def __aenter__(self):
        await self.create_bucket()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def unpack(self):
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
            config=self.config,
        ) as client:
            yield {
                "client": client,
                "bucket_name": self.bucket_name,
            }


class S3Connection(S3ConnectionBase):
    def __init__(
        self,
        endpoint: str = S3_ENDPOINT,
        access_key: str = S3_ACCESS_KEY,
        secret_key: str = S3_SECRET_KEY,
        region_name: str = S3_REGION_NAME,
        bucket_name: str = S3_BUCKET_NAME,
    ):
        super().__init__(endpoint, access_key, secret_key, region_name, bucket_name)
