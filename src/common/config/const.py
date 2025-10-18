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

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "broker-1:19092,broker-2:19092,broker-3:19092"
)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgresadmin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "supersecret!")
POSTGRES_DB = os.getenv("POSTGRES_DB", "default")

MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_USER = os.getenv("MONGO_USER", "mongoadmin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "supersecret!")
MONGO_DB = os.getenv("MONGO_DB", "default")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_USER = os.getenv("REDIS_USER", "default")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "supersecret!")
REDIS_DB = os.getenv("REDIS_DB", "0")

NEO4J_HOST = os.getenv("NEO4J_HOST", "neo4j")
NEO4J_PORT = os.getenv("NEO4J_PORT", "7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "supersecret!")
NEO4J_DB = os.getenv("NEO4J_DB", "default")

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://s3:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minioadmin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minioadmin")
S3_REGION_NAME = os.getenv("S3_REGION_NAME", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "default")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "rabbitadmin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "rabbitadmin")
RABBITMQ_VHOST = os.getenv("RABBITMQ_PASSWORD", "default")

CELERY_RABBITMQ_HOST = os.getenv("CELERY_RABBITMQ_HOST", RABBITMQ_HOST)
CELERY_RABBITMQ_PORT = os.getenv("CELERY_RABBITMQ_PORT", RABBITMQ_PORT)
CELERY_RABBITMQ_USER = os.getenv("CELERY_RABBITMQ_USER", RABBITMQ_USER)
CELERY_RABBITMQ_PASSWORD = os.getenv("CELERY_RABBITMQ_PASSWORD", RABBITMQ_PASSWORD)
CELERY_RABBITMQ_VHOST = os.getenv("CELERY_RABBITMQ_VHOST", RABBITMQ_VHOST)

CELERY_REDIS_HOST = os.getenv("CELERY_REDIS_HOST", REDIS_HOST)
CELERY_REDIS_PORT = os.getenv("CELERY_REDIS_PORT", REDIS_PORT)
CELERY_REDIS_USER = os.getenv("CELERY_REDIS_USER", REDIS_USER)
CELERY_REDIS_PASSWORD = os.getenv("CELERY_REDIS_PASSWORD", REDIS_PASSWORD)
CELERY_REDIS_DB = os.getenv("CELERY_REDIS_DB", "1")
