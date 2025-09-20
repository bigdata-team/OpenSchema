import os

from botocore.config import Config
import aioboto3

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")


def get_s3():
    return aioboto3.Session().client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION_NAME,
        config=Config(s3={"addressing_style": "path"}),
    )
