import os
from typing import Any

import motor.motor_asyncio
from beanie import init_beanie

from common.models.db import Document

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"


async def get_mongo() -> Any:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    return client[MONGO_DB]


async def init_mongo():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client[MONGO_DB], document_models=[Document])
