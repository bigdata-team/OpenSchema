from common.config import NEO4J_DB, NEO4J_HOST, NEO4J_PASSWORD, NEO4J_PORT, NEO4J_USER

from .connection import ConnectionBase


class Neo4jConnectionBase(ConnectionBase):
    def __init__(
        self,
        host: str,
        port: str,
        user: str,
        password: str,
        db: str,
    ):
        from neo4j import AsyncGraphDatabase

        self.url = f"bolt://{host}:{port}"
        self.db = db
        self.driver = AsyncGraphDatabase.driver(self.url, auth=(user, password))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.driver.close()

    async def unpack(self):
        async with self.driver.session(database=self.db) as session:
            yield session


class Neo4jConnection(Neo4jConnectionBase):
    def __init__(
        self,
        host: str = NEO4J_HOST,
        port: str = NEO4J_PORT,
        user: str = NEO4J_USER,
        password: str = NEO4J_PASSWORD,
        db: str = NEO4J_DB,
    ):
        super().__init__(host, port, user, password, db)
