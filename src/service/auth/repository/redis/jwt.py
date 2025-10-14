from fastapi import Depends

from common.connection import get_session
from common.connection.redis import RedisConnection
from common.repository.redis import RedisRepository


class JwtRepository(RedisRepository[str]):
    def __init__(self, redis=Depends(get_session(RedisConnection))):
        super().__init__(str, redis)
