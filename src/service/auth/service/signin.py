from fastapi import Depends
from model.http.signin import SignInResponse
from repository.sql.user import UserRepository

from common.config import JWT_REFRESH_TOKEN_TTL, SERVICE_NAME, SERVICE_VERSION
from common.model.http import create_response
from common.util.jwt import claim_tokens
from common.util.password import verify_password


class SignInService:
    def __init__(self, repo: UserRepository = Depends(UserRepository)):
        self.repo = repo

    async def signin(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user:
            return self._unauthorized()

        if not verify_password(password, user.hashed_password):
            return self._unauthorized()

        return await self.issue(user.id, detail="Sign in successful.")

    @staticmethod
    async def issue(user_id: str, detail="Sign in successful."):
        access_token, refresh_token = claim_tokens(user_id)
        data = SignInResponse(access_token=access_token, refresh_token=refresh_token)

        response = create_response(code=200, detail=detail, data=data)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            path=f"/api/{SERVICE_VERSION}/{SERVICE_NAME}/refresh",
            max_age=JWT_REFRESH_TOKEN_TTL,
        )
        return response

    @staticmethod
    def _unauthorized():
        return create_response(code=401, detail="Invalid credentials")
