import os
from typing import Any

import motor.motor_asyncio

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"


async def get_mongo() -> Any:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    return client[MONGO_DB]
