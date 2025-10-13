import logging
from logging.config import dictConfig
from typing import Any, Dict

from common.model.log import Log
from common.config.const import LOG_LEVEL, SERVICE_NAME

DEFAULT_LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {},
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"],
    },
}


def configure_logging(log_level: str):
    config = DEFAULT_LOGGING_CONFIG.copy()
    config["loggers"]["app"] = {
        "level": log_level,
        "handlers": ["console"],
        "propagate": False,
    }
    dictConfig(config)


class logger:
    _logger = logging.getLogger("app")

    @classmethod
    def debug(cls, msg: str, crid: str):
        model = Log(level="debug", crid=crid, msg=msg)
        cls._logger.debug(model.model_dump_json())

    @classmethod
    def info(cls, msg: str, crid: str):
        model = Log(level="info", crid=crid, msg=msg)
        cls._logger.info(model.model_dump_json())

    @classmethod
    def warning(cls, msg: str, crid: str):
        model = Log(level="warning", crid=crid, msg=msg)
        cls._logger.warning(model.model_dump_json())

    @classmethod
    def error(cls, msg: str, crid: str):
        model = Log(level="error", crid=crid, msg=msg)
        cls._logger.error(model.model_dump_json())

    @classmethod
    def critical(cls, msg: str, crid: str):
        model = Log(level="critical", crid=crid, msg=msg)
        cls._logger.critical(model.model_dump_json())
