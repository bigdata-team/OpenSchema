import os

from ._base import AsyncConnection, Connection, Registry, unpack


class KafkaConnection(Connection):
    def __init__(
        self,
        key: str = None,
        bootstrap_servers: list[str] = os.getenv("KAFKA_BOOTSTRAP_SERVERS").split(","),
    ):
        from kafka import KafkaProducer

        self.bootstrap_servers = bootstrap_servers
        self.key = key or f"sync.kafka.{'.'.join(sorted(self.bootstrap_servers))}"

        if not Registry.has(self.key):
            session = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
            Registry.register(self.key, {"session": session})

        self.session: KafkaProducer = Registry.get(self.key)["session"]

    def connect(self):
        import time

        return self.session.send(
            "connect", f"[sync.kafka.connect] {time.time()}".encode()
        ).get()


class AsyncKafkaConnection(AsyncConnection):
    def __init__(
        self,
        key: str = None,
        bootstrap_servers: list[str] = os.getenv("KAFKA_BOOTSTRAP_SERVERS").split(","),
    ):
        from aiokafka import AIOKafkaProducer

        self.bootstrap_servers = bootstrap_servers
        self.key = key or f"async.kafka.{'.'.join(sorted(self.bootstrap_servers))}"

        if not Registry.has(self.key):
            session = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            Registry.register(self.key, {"session": session, "started": False})

        reg = Registry.get(self.key)
        self.session: AIOKafkaProducer = reg["session"]
        self._reg = reg

    async def connect(self):
        import time

        if not self._reg.get("started", False):
            await self.session.start()
            self._reg["started"] = True

        return await self.session.send_and_wait(
            "connect", f"[async.kafka.connect] {time.time()}".encode()
        )
