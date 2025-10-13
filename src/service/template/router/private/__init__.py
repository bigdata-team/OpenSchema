from fastapi import APIRouter, Depends

from common.middleware.authorization import get_auth_dependency
from common.model.http import create_response

router = APIRouter(
    tags=["private"],
    dependencies=[
        Depends(
            get_auth_dependency(
                auth_header="Authorization",
                token_prefix="Bearer ",
                issuer="auth.service",
                audience="service",
            )
        ),
    ],
)


@router.get("/_ping")
async def ping():
    return create_response(message="pong")
