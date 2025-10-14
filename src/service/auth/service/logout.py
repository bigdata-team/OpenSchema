from fastapi import Depends, Request
from repository.redis.jwt import JwtRepository

from common.config import JWT_REFRESH_TOKEN_TTL, SERVICE_API_VERSION, SERVICE_NAME
from common.model.http import create_response


class LogoutService:
    def __init__(
        self,
        request: Request,
        repo: JwtRepository = Depends(JwtRepository),
    ):
        self.request = request
        self.repo = repo

    async def logout(self, sid: str | None = None):
        sid = sid or self.request.state.token_payload.sid
        if not sid:
            return create_response(code=400, detail="No session ID provided")

        await self.repo.create_or_update(
            f"bl:jwt:sid:{sid}", "blacklisted", ttl=JWT_REFRESH_TOKEN_TTL
        )
        response = create_response(code=200, detail="Logged out")
        response.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            secure=True,
            path=f"/api/{SERVICE_API_VERSION}/{SERVICE_NAME}/refresh",
            max_age=0,
        )
        return response
