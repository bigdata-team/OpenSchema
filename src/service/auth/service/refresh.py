from fastapi import Depends, Request
from repository.redis.jwt import JwtRepository
from service.signin import SignInService

from common.config import JWT_REFRESH_TOKEN_TTL, SERVICE_VERSION, SERVICE_NAME
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
        cookie_payload = verify_token(self.request.cookies.get("refresh_token"))
        header_payload = self.request.state.token_payload
        print("****************")
        print(cookie_payload)
        print("****************")
        print(header_payload)
        print("****************")

        payload = cookie_payload or header_payload or None

        if isinstance(payload, RefreshTokenPayload):
            if await self.repo.get(f"bl:jwt:{payload.sid}"):
                return create_response(code=401, detail="Unauthorized")

            await self.repo.create_or_update(
                f"bl:jwt:{payload.sid}", "blacklisted", ttl=JWT_REFRESH_TOKEN_TTL
            )
            return await SignInService.issue(
                user_id=payload.sub, detail="Token refreshed."
            )

        return create_response(code=401, detail="Unauthorized")
