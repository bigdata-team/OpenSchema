import os

from neo4j import AsyncGraphDatabase

NEO4J_HOST = os.getenv("NEO4J_HOST")
NEO4J_PORT = int(os.getenv("NEO4J_PORT"))
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


def get_neo4j():
    return AsyncGraphDatabase.driver(
        f"bolt://{NEO4J_HOST}:{NEO4J_PORT}",
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )
