import asyncio

from common.connection.kafka import consume
from common.log import create_logger

logger = create_logger(name="template-worker")


handlers = {"template.healthz": lambda x: x}


def main() -> None:
    asyncio.run(consume(handlers, group_id="template-group"))


if __name__ == "__main__":
    main()
