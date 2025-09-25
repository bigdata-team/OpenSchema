import os

from neo4j import AsyncGraphDatabase

NEO4J_HOST = os.getenv("NEO4J_HOST")
NEO4J_PORT = int(os.getenv("NEO4J_PORT"))
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


def get_aioneo4j(
    host=NEO4J_HOST, port=NEO4J_PORT, user=NEO4J_USER, password=NEO4J_PASSWORD
):
    uri = f"bolt://{host}:{port}"
    return AsyncGraphDatabase.driver(
        uri,
        auth=(user, password),
    )
