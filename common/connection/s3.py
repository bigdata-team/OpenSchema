import os
from ._base import unpack, Connection, AsyncConnection, Registry


class S3Connection(Connection):
    def __init__(
        self,
        key: str = None,
        endpoint_url: str = os.getenv("S3_ENDPOINT"),
        aws_access_key_id: str = os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key: str = os.getenv("S3_SECRET_KEY"),
        region_name: str = os.getenv("S3_REGION_NAME"),
    ):
        import boto3
        from botocore.config import Config

        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.key = (
            key
            or f"sync.s3.{self.aws_access_key_id}.{self.aws_secret_access_key}.{self.endpoint_url}.{self.region_name}"
        )

        self.config = Config(s3={"addressing_style": "path"})

        if not Registry.has(self.key):
            session = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name,
                config=self.config,
            )
            Registry.register(self.key, {"session": session})

        self.session = Registry.get(self.key)["session"]

    def connect(self):
        return self.session.list_buckets()


class AsyncS3Connection(AsyncConnection):
    def __init__(
        self,
        key: str = None,
        endpoint_url: str = os.getenv("S3_ENDPOINT"),
        aws_access_key_id: str = os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key: str = os.getenv("S3_SECRET_KEY"),
        region_name: str = os.getenv("S3_REGION_NAME"),
    ):
        import aioboto3
        from botocore.config import Config

        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.key = (
            key
            or f"async.s3.{self.aws_access_key_id}.{self.aws_secret_access_key}.{self.endpoint_url}.{self.region_name}"
        )

        self.config = Config(s3={"addressing_style": "path"})

        self.session: aioboto3.Session = None

        self._session = aioboto3.Session()
        self._client = None

    async def __aenter__(self):
        self._client = self._session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            config=self.config,
        )
        self.session = await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        try:
            await self._client.__aexit__(exc_type, exc_value, traceback)
        finally:
            self.session = None
            self._client = None

    @unpack
    async def connect(self):
        return await self.session.list_buckets()
