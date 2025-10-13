from celery import Celery
from kombu import Queue
from common.config.const import SERVICE_NAME
from common.config.const import (
    CELERY_RABBITMQ_HOST,
    CELERY_RABBITMQ_PASSWORD,
    CELERY_RABBITMQ_USER,
    CELERY_RABBITMQ_PORT,
    CELERY_RABBITMQ_VHOST,
)
from common.config.const import (
    CELERY_REDIS_HOST,
    CELERY_REDIS_PASSWORD,
    CELERY_REDIS_USER,
    CELERY_REDIS_PORT,
    CELERY_REDIS_DB,
)


BROKER_URL = f"amqp://{CELERY_RABBITMQ_USER}:{CELERY_RABBITMQ_PASSWORD}@{CELERY_RABBITMQ_HOST}:{CELERY_RABBITMQ_PORT}/{CELERY_RABBITMQ_VHOST}"
BACKEND_URL = f"redis://{CELERY_REDIS_USER}:{CELERY_REDIS_PASSWORD}@{CELERY_REDIS_HOST}:{CELERY_REDIS_PORT}/{CELERY_REDIS_DB}"


worker = Celery(
    SERVICE_NAME,
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=[
        "job",
        "common.celery.job",
    ],
)


worker.conf.update(
    task_default_queue=SERVICE_NAME,
    task_queues=(Queue(SERVICE_NAME),),
    task_routes={
        "job.*": {"queue": SERVICE_NAME},
        "common.celery.job.*": {"queue": SERVICE_NAME},
    },
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
    task_track_started=True,
    broker_connection_retry_on_startup=True,
)

# try:
#     worker.autodiscover_tasks(packages=["common.celery", "job"])
# except Exception:
#     # Safe no-op if packages aren't packages or discovery not needed
#     pass
