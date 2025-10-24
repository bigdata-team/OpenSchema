from fastapi import APIRouter, Depends
from model.http.signin import SignInResponse
from service.refresh import RefreshService

from common.middleware.authorization import get_auth_dependency
from common.model.http import DataBody

router = APIRouter(
    tags=["protected"],
    dependencies=[
        Depends(get_auth_dependency(strict=False)),
    ],
)


@router.get("/refresh", response_model=DataBody[SignInResponse])
async def refresh(service: RefreshService = Depends(RefreshService)):
    return await service.refresh()
