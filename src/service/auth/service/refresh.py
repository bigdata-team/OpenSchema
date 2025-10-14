from fastapi import Depends, Request
from repository.redis.jwt import JwtRepository
from service.login import LoginService

from common.config import JWT_REFRESH_TOKEN_TTL, SERVICE_API_VERSION, SERVICE_NAME
from common.model.http import create_response
from common.model.jwt import RefreshTokenPayload
from common.util.jwt import verify_token


class RefreshService:
    def __init__(
        self,
        request: Request,
        repo: JwtRepository = Depends(JwtRepository),
    ):
        self.request = request
        self.repo = repo

    async def refresh(self):
        header_payload = self.request.state.token_payload
        cookie_payload = None
        if not header_payload:
            cookie_payload = verify_token(self.request.cookies.get("refresh_token"))

        payload = header_payload or cookie_payload or None

        if isinstance(payload, RefreshTokenPayload):
            if await self.repo.get(f"bl:jwt:{payload.sid}"):
                return create_response(code=401, detail="Unauthorized")

            await self.repo.create_or_update(
                f"bl:jwt:{payload.sid}", "blacklisted", ttl=JWT_REFRESH_TOKEN_TTL
            )
            return await LoginService.issue(
                user_id=payload.sub, detail="Token refreshed."
            )

        return create_response(code=401, detail="Unauthorized")
