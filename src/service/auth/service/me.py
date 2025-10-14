from fastapi import Depends, Request
from repository.redis.jwt import JwtRepository
from repository.sql.user import UserRepository
from service.login import LoginService

from common.config import JWT_REFRESH_TOKEN_TTL, SERVICE_API_VERSION, SERVICE_NAME
from common.model.http import create_response
from common.model.jwt import RefreshTokenPayload
from common.util.jwt import verify_token


class MeService:
    def __init__(
        self,
        request: Request,
        jwt_repo: JwtRepository = Depends(JwtRepository),
        user_repo: UserRepository = Depends(UserRepository),
    ):
        self.request = request
        self.jwt_repo = jwt_repo
        self.user_repo = user_repo

    async def info(self):
        if await self.jwt_repo.get(f"bl:jwt:{self.request.state.token_payload.sid}"):
            return create_response(code=401, detail="Unauthorized")

        user = await self.user_repo.get(self.request.state.token_payload.sub)
        if user is None:
            return create_response(code=404, detail="User not found")
        return create_response(code=200, detail="User info", data=user)
