import os
from typing import Literal

PROJECT_NAME = os.getenv("PROJECT_NAME", "OpenSchema")

LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = os.getenv(
    "LOG_LEVEL", "INFO"
)

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ENCODE_SECRET = os.getenv("JWT_ENCODE_SECRET", "supersecret!")
JWT_DECODE_SECRET = os.getenv("JWT_DECODE_SECRET", "supersecret!")
JWT_ACCESS_TOKEN_TTL = int(os.getenv("JWT_ACCESS_TOKEN_TTL", "180"))
JWT_REFRESH_TOKEN_TTL = int(os.getenv("JWT_REFRESH_TOKEN_TTL", "86400"))

SERVICE_ID = os.getenv("SERVICE_ID")
SERVICE_NAME = os.getenv("SERVICE_NAME")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "v1")
SERVICE_TYPE = os.getenv("SERVICE_TYPE", "api")
SERVICE_DB_SCHEMA = os.getenv("SERVICE_DB_SCHEMA", SERVICE_NAME)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:19092")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgresadmin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "supersecret!")
POSTGRES_DB = os.getenv("POSTGRES_DB", "default")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_USER = os.getenv("REDIS_USER", "default")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "supersecret!")
REDIS_DB = os.getenv("REDIS_DB", "0")

CELERY_REDIS_HOST = os.getenv("CELERY_REDIS_HOST", REDIS_HOST)
CELERY_REDIS_PORT = os.getenv("CELERY_REDIS_PORT", REDIS_PORT)
CELERY_REDIS_USER = os.getenv("CELERY_REDIS_USER", REDIS_USER)
CELERY_REDIS_PASSWORD = os.getenv("CELERY_REDIS_PASSWORD", REDIS_PASSWORD)
CELERY_REDIS_DB = os.getenv("CELERY_REDIS_DB", "1")

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# elpai auth
ELPAI_AUTH_URL = os.getenv("ELPAI_AUTH_URL")
