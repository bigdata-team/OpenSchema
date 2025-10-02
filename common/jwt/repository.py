import time
from common.repository import AsyncRedisRepository
from common.jwt.model import TokenPayload, create_blacklist_value


class JwtRepository(AsyncRedisRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def add_blacklist(self, payload: TokenPayload):
        self.session.setex(
            name=create_blacklist_value(payload.sid),
            time=payload.exp - int(time.time()),
            value="blacklisted",
        )

    async def is_blacklisted(self, payload: TokenPayload) -> bool:
        return self.session.exists(create_blacklist_value(payload.sid))
