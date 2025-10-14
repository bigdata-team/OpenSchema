from common.config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

from .sql import create_sql_lifespan, get_sql_session


def create_postgres_lifespan(
    key: str = "postgres",
    host: str = POSTGRES_HOST,
    port: str = POSTGRES_PORT,
    user: str = POSTGRES_USER,
    password: str = POSTGRES_PASSWORD,
    db: str = POSTGRES_DB,
):
    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    lifespan = create_sql_lifespan(key, url)
    return lifespan


def get_postgres_session(key: str = "postgres"):
    return get_sql_session(key)
