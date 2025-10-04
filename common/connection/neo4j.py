import os
from ._base import unpack, Connection, AsyncConnection, Registry
from common.util.hash import sha1


class Neo4jConnection(Connection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("NEO4J_HOST"),
        port: str = os.getenv("NEO4J_PORT"),
        user: str = os.getenv("NEO4J_USER"),
        password: str = os.getenv("NEO4J_PASSWORD"),
        db: str = os.getenv("NEO4J_DB"),
    ):
        from neo4j import GraphDatabase, Session

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

        self.key = key or f"sync.neo4j.{self.host}.{self.port}.{self.user}.{self.db}"

        if not Registry.has(self.key):
            driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            Registry.register(
                self.key,
                {
                    "driver": driver,
                },
            )

        self.driver = Registry.get(self.key)["driver"]
        self.session: Session = None

    @property
    def uri(self):
        return f"bolt://{self.host}:{self.port}"

    def __enter__(self):
        self.session = self.driver.session(database=self.db)
        self.session.__enter__()
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        try:
            if exc_type:
                pass
        finally:
            if self.session:
                self.session.close()
            self.session = None

    @unpack
    def connect(self):
        return self.session.run("RETURN 1")


class AsyncNeo4jConnection(AsyncConnection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("NEO4J_HOST"),
        port: str = os.getenv("NEO4J_PORT"),
        user: str = os.getenv("NEO4J_USER"),
        password: str = os.getenv("NEO4J_PASSWORD"),
        db: str = os.getenv("NEO4J_DB"),
    ):
        from neo4j import AsyncGraphDatabase, AsyncSession

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

        self.key = key or f"async.neo4j.{self.host}.{self.port}.{self.user}.{self.db}"

        if not Registry.has(self.key):
            driver = AsyncGraphDatabase.driver(
                self.uri, auth=(self.user, self.password)
            )
            Registry.register(
                self.key,
                {
                    "driver": driver,
                },
            )

        self.driver = Registry.get(self.key)["driver"]
        self.session: AsyncSession = None

    @property
    def uri(self):
        return f"bolt://{self.host}:{self.port}"

    async def __aenter__(self):
        self.session = self.driver.session(database=self.db)
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        try:
            if exc_type:
                pass
        finally:
            if self.session:
                await self.session.close()
            self.session = None

    @unpack
    async def connect(self):
        return await self.session.run("RETURN 1")
