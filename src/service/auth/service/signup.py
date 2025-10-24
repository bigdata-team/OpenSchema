from fastapi import Depends
from model.sql import User
from repository.sql.user import UserRepository

from common.model.http import create_response
from common.util.password import hash_password


class SignUpService:
    def __init__(self, repo: UserRepository = Depends(UserRepository)):
        self.repo = repo

    async def signup(self, email: str, password: str):
        prev_user = await self.repo.get_by_email(email)
        if prev_user:
            return create_response(code=409, detail="User already exists")

        password = hash_password(password)
        user = User(email=email, hashed_password=password)
        await self.repo.create(user)

        return create_response(code=201, detail="User created", data=user)
