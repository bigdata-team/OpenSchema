from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Request

from common.config import KAFKA_BOOTSTRAP_SERVERS


def create_kafka_lifespan(
    key: str = "kafka",
    bootstrap_servers: list[str] = KAFKA_BOOTSTRAP_SERVERS.split(","),
):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "connection"):
            app.state.connection = {}

        session = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        await session.start()
        app.state.connection[key] = {
            "session": session,
        }
        yield
        try:
            await session.flush()
        finally:
            await session.stop()

    return lifespan


def get_kafka_session(key: str = "kafka"):
    async def _unpack(request: Request) -> AIOKafkaProducer:
        resource = request.app.state.connection[key]
        return resource.get("session")

    return _unpack
