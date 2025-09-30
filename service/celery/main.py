from common.connection.celery import get_celery_worker

worker = get_celery_worker()
worker.autodiscover_tasks(["common.jobs"])
