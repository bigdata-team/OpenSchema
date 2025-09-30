import os

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS").split(",")


def get_aiokafka_producer(bootstrap_servers: list[str] = KAFKA_BOOTSTRAP_SERVERS):
    return AIOKafkaProducer(bootstrap_servers=bootstrap_servers)


def get_aiokafka_consumer(
    topics: list[str],
    group_id: str,
    bootstrap_servers: list[str] = KAFKA_BOOTSTRAP_SERVERS,
):
    return AIOKafkaConsumer(
        *topics, bootstrap_servers=bootstrap_servers, group_id=group_id
    )


# async def consume(handlers: dict[callable], group_id: str):
#     consumer = create_aiokafka_consumer(handlers.keys(), group_id)
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             handlers[msg.topic](msg.value)
#     finally:
#         await consumer.stop()
