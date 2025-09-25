from celery import Celery
import os

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
CELERY_REDIS_DB = os.getenv("CELERY_REDIS_DB")


def get_worker():
    return Celery(
        "celery.service",
        broker=f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//",
        backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_REDIS_DB}",
    )


def get_client(name: str):
    return Celery(
        name,
        broker=f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//",
    )
