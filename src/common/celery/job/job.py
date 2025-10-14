import time

from celery.utils.log import get_task_logger

from common.celery.worker import worker


@worker.task
def greet(msg):
    time.sleep(15)
    return f"Hello, {msg}!"
