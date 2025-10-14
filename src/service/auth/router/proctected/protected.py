from fastapi import APIRouter, Depends, Request
from model.http.login import LoginRequest, LoginResponse
from model.http.register import RegisterRequest
from model.sql import User
from service.login import LoginService
from service.refresh import RefreshService
from service.register import RegisterService

from common.middleware.authorization import get_auth_dependency
from common.model.http import DataBody, create_response
from common.util.jwt import verify_token

router = APIRouter(
    tags=["protected"],
    dependencies=[
        Depends(get_auth_dependency(strict=False)),
    ],
)


@router.post("/refresh", response_model=DataBody[LoginResponse])
async def login(service: RefreshService = Depends(RefreshService)):
    return await service.refresh()
