from fastapi import APIRouter, Depends, Request
from model.http.login import LoginResponse
from service.login import LoginService
from service.logout import LogoutService
from service.me import MeService
from service.register import RegisterService

from common.middleware.authorization import get_auth_dependency
from common.model.http import DataBody, create_response

router = APIRouter(
    tags=["private"],
    dependencies=[
        Depends(get_auth_dependency()),
    ],
)


@router.get("/_ping")
async def ping(request: Request):
    return create_response(detail="pong", data=request.state.token_payload)


@router.get("/logout")
async def logout(service: LogoutService = Depends(LogoutService)):
    return await service.logout()


@router.get("/me")
async def me(
    service: MeService = Depends(MeService),
):
    return await service.info()
