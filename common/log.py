import json
import logging
import os
import sys
from logging import Logger as L

from .utils import Now

# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.DEBUG)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        body = record.getMessage()
        try:
            body = json.loads(body)
        except:
            pass
        log_record = {
            "ts": Now().iso,
            "level": record.levelname,
            "logger": record.name,
            "body": body,
        }
        return json.dumps(log_record, ensure_ascii=False)


def create_logger(name, level=LOG_LEVEL):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    logger.propagate = False
    return logger
