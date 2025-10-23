from common.celery.worker import worker


@worker.task
def add(x, y):
    return str(x) + str(y)
