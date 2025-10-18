from fastapi import Depends
from service.chat.model.sql.history import History
from repository.sql.history import HistoryRepository

from common.model.http import create_response
from common.util.password import hash_password


class RegisterService:
    def __init__(self, repo: HistoryRepository = Depends(HistoryRepository)):
        self.repo = repo
    
    async def 

    async def register(self, email: str, password: str):
        prev_user = await self.repo.get_by_email(email)
        if prev_user:
            return create_response(code=409, detail="User already exists")

        password = hash_password(password)
        user = (email=email, hashed_password=password)
        user = await self.repo.create(user)

        return create_response(code=201, detail="User created")
