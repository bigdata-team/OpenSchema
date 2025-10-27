""" TODO
import uuid
def generate_id() -> str:
    return str(uuid.uuid4())
"""

from common.util.random.random import new_id
def generate_id() -> str:
    return new_id()