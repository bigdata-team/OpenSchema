from common.connection.celery import get_worker

worker = get_worker()
worker.autodiscover_tasks(["common.jobs"])