from fastapi import APIRouter, Depends, Request

from common.middleware.authorization import get_require_auth
from common.model.http import create_response

router = APIRouter(tags=["private"], dependencies=[Depends(get_require_auth())])


@router.get("/private-ping")
async def ping(request: Request):
    return create_response("pong", data=request.state.token_payload)
