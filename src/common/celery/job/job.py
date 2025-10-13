from common.celery.worker import worker

from celery.utils.log import get_task_logger

import time


@worker.task
def greet(msg):
    time.sleep(15)
    return f"Hello, {msg}!"
