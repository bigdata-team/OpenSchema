import os

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS").split(",")


def create_kafka_producer():
    return AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)


def create_kafka_consumer(topics: list[str], group_id: str):
    return AIOKafkaConsumer(
        *topics, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=group_id
    )


async def consume(handlers: dict[callable], group_id: str):
    consumer = create_kafka_consumer(handlers.keys(), group_id)
    await consumer.start()
    try:
        async for msg in consumer:
            handlers[msg.topic](msg.value)
    finally:
        await consumer.stop()
