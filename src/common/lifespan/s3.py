from contextlib import asynccontextmanager
from typing import Any

import aioboto3
from botocore.config import Config
from fastapi import FastAPI, Request

from common.config import (
    S3_ACCESS_KEY,
    S3_BUCKET_NAME,
    S3_ENDPOINT,
    S3_REGION_NAME,
    S3_SECRET_KEY,
)


async def _create_bucket(client: Any, bucket_name: str, region_name: str):
    existing_buckets = await client.list_buckets()
    bucket_names = [bucket["Name"] for bucket in existing_buckets.get("Buckets", [])]

    if bucket_name not in bucket_names:
        create_kwargs = {"Bucket": bucket_name}
        if region_name and region_name != "us-east-1":
            create_kwargs["CreateBucketConfiguration"] = {
                "LocationConstraint": region_name
            }
        await client.create_bucket(**create_kwargs)


def create_s3_lifespan(
    key: str = "s3",
    endpoint: str = S3_ENDPOINT,
    access_key: str = S3_ACCESS_KEY,
    secret_key: str = S3_SECRET_KEY,
    region_name: str = S3_REGION_NAME,
    bucket_name: str = S3_BUCKET_NAME,
):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "connection"):
            app.state.connection = {}

        session = aioboto3.Session()
        config = Config(s3={"addressing_style": "path"})

        client_kwargs = {
            "endpoint_url": endpoint,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "region_name": region_name,
            "config": config,
        }

        async with session.client("s3", **client_kwargs) as client:
            await _create_bucket(client, bucket_name, region_name)

        app.state.connection[key] = {
            "session": session,
            "client_kwargs": client_kwargs,
            "bucket_name": bucket_name,
        }
        yield

    return lifespan


def get_s3_session(key: str = "s3"):
    async def _unpack(request: Request):
        resource = request.app.state.connection[key]
        async with resource["session"].client(
            "s3", **resource["client_kwargs"]
        ) as client:
            yield {
                "client": client,
                "bucket_name": resource.get("bucket_name"),
            }

    return _unpack
