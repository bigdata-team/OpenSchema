from fastapi import APIRouter, Depends, Request
from service.me import MeService
from service.signout import SignOutService
from model.sql import User

from common.middleware.authorization import get_auth_dependency
from common.model.http import create_response, DataBody, Body

router = APIRouter(
    tags=["private"],
    dependencies=[
        Depends(get_auth_dependency()),
    ],
)


@router.get("/_ping")
async def ping(request: Request):
    return create_response(detail="pong", data=request.state.token_payload)


@router.post("/signout", response_model=Body)
async def signout(service: SignOutService = Depends(SignOutService)):
    return await service.signout()


""" TODO
@router.get("/me", response_model=DataBody[User])
async def me(
    service: MeService = Depends(MeService),
):
    return await service.info()
"""