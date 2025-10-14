import asyncio

from common.config import KAFKA_BOOTSTRAP_SERVERS

from .connection import ConnectionBase


class KafkaConnectionBase(ConnectionBase):
    def __init__(self, bootstrap_servers: list[str]):
        self.bootstrap_servers = bootstrap_servers
        self._producer = None
        self._producer_lock = None
        self._started = False

    async def _ensure_producer(self):
        from aiokafka import AIOKafkaProducer

        if self._producer_lock is None:
            self._producer_lock = asyncio.Lock()

        async with self._producer_lock:
            if self._producer is None:
                self._producer = AIOKafkaProducer(
                    bootstrap_servers=self.bootstrap_servers
                )
            if not self._started:
                await self._producer.start()
                self._started = True

        return self._producer

    async def __aenter__(self):
        await self._ensure_producer()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._producer or not self._started:
            return

        try:
            await self._producer.flush()
        finally:
            await self._producer.stop()
            self._started = False
            self._producer = None

    async def unpack(self):
        producer = await self._ensure_producer()
        return producer


class KafkaConnection(KafkaConnectionBase):
    def __init__(
        self, bootstrap_servers: list[str] = KAFKA_BOOTSTRAP_SERVERS.split(",")
    ):
        super().__init__(bootstrap_servers)
