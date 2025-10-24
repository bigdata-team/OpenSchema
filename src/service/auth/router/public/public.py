from fastapi import APIRouter, Depends
from model.http.signin import SignInRequest, SignInResponse
from model.http.signup import SignUpRequest
from model.sql import User
from service.signin import SignInService
from service.signup import SignUpService

from common.model.http import Body, DataBody, create_response

router = APIRouter(tags=["public"])


@router.get("/ping", response_model=Body)
async def ping():
    return create_response(detail="pong")


@router.post("/signup", response_model=DataBody[User])
async def signup(body: SignUpRequest, service: SignUpService = Depends(SignUpService)):
    return await service.signup(body.email, body.password)


@router.post("/signin", response_model=DataBody[SignInResponse])
async def signin(body: SignInRequest, service: SignInService = Depends(SignInService)):
    return await service.signin(body.email, body.password)
