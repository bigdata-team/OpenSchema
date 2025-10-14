from fastapi import APIRouter, Depends, Request
from model.http.login import LoginRequest, LoginResponse
from model.http.register import RegisterRequest
from model.sql import User
from service.login import LoginService
from service.register import RegisterService

from common.model.http import DataBody, create_response

router = APIRouter(tags=["public"])


@router.get("/ping")
async def ping():
    return create_response(detail="pong")


@router.post("/register", response_model=DataBody[User])
async def register(
    body: RegisterRequest, service: RegisterService = Depends(RegisterService)
):
    return await service.register(body.email, body.password)


@router.post("/login", response_model=DataBody[LoginResponse])
async def login(body: LoginRequest, service: LoginService = Depends(LoginService)):
    return await service.login(body.email, body.password)
