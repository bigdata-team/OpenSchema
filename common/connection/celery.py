import os

from celery import Celery

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "rabbitadmin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "rabbitadmin")

CELERY_RABBITMQ_HOST = os.getenv("CELERY_RABBITMQ_HOST", RABBITMQ_HOST)
CELERY_RABBITMQ_PORT = os.getenv("CELERY_RABBITMQ_PORT", RABBITMQ_PORT)
CELERY_RABBITMQ_USER = os.getenv("CELERY_RABBITMQ_USER", RABBITMQ_USER)
CELERY_RABBITMQ_PASSWORD = os.getenv("CELERY_RABBITMQ_PASSWORD", RABBITMQ_PASSWORD)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

CELERY_REDIS_HOST = os.getenv("CELERY_REDIS_HOST", REDIS_HOST)
CELERY_REDIS_PORT = os.getenv("CELERY_REDIS_PORT", REDIS_PORT)
CELERY_REDIS_PASSWORD = os.getenv("CELERY_REDIS_PASSWORD", REDIS_PASSWORD)
CELERY_REDIS_DB = os.getenv("CELERY_REDIS_DB", "1")


def get_celery_worker(
    name: str = "celery.worker",
    rabbitmq_host: str = CELERY_RABBITMQ_HOST,
    rabbitmq_port: str = CELERY_RABBITMQ_PORT,
    rabbitmq_user: str = CELERY_RABBITMQ_USER,
    rabbitmq_password: str = CELERY_RABBITMQ_PASSWORD,
    redis_host: str = CELERY_REDIS_HOST,
    redis_port: str = CELERY_REDIS_PORT,
    redis_password: str = CELERY_REDIS_PASSWORD,
    redis_db: str = CELERY_REDIS_DB,
):
    broker_uri = (
        f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}//"
    )
    backend_uri = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
    return Celery(name, broker=broker_uri, backend=backend_uri)


def get_celery_client(
    name: str = "celery.client",
    rabbitmq_host: str = CELERY_RABBITMQ_HOST,
    rabbitmq_port: str = CELERY_RABBITMQ_PORT,
    rabbitmq_user: str = CELERY_RABBITMQ_USER,
    rabbitmq_password: str = CELERY_RABBITMQ_PASSWORD,
):
    broker_uri = (
        f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}//"
    )
    return Celery(name, broker=broker_uri)
