import os

from ._base import AsyncConnection, Connection, Registry, unpack
from .sqlalchemy import AsyncSQLConnection, SQLConnection


class PostgresConnection(SQLConnection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("POSTGRES_HOST"),
        port: str = os.getenv("POSTGRES_PORT"),
        user: str = os.getenv("POSTGRES_USER"),
        password: str = os.getenv("POSTGRES_PASSWORD"),
        db: str = os.getenv("POSTGRES_DB"),
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        uri = f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        key = key or f"sync.postgres.{self.host}.{self.port}.{self.user}.{self.db}"

        super().__init__(uri=uri, key=key)


class AsyncPostgresConnection(AsyncSQLConnection):
    def __init__(
        self,
        key: str = None,
        host: str = os.getenv("POSTGRES_HOST"),
        port: str = os.getenv("POSTGRES_PORT"),
        user: str = os.getenv("POSTGRES_USER"),
        password: str = os.getenv("POSTGRES_PASSWORD"),
        db: str = os.getenv("POSTGRES_DB"),
    ):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        uri = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        key = key or f"async.postgres.{self.host}.{self.port}.{self.user}.{self.db}"

        super().__init__(uri=uri, key=key)
