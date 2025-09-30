import os

import motor.motor_asyncio

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


async def get_aiomongo(
    host=MONGO_HOST,
    port=MONGO_PORT,
    user=MONGO_USER,
    password=MONGO_PASSWORD,
    db=MONGO_DB,
):
    uri = f"mongodb://{user}:{password}@{host}:{port}"
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    return client[db]
