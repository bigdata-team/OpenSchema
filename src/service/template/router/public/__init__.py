from fastapi import APIRouter, Depends

from common.model.http import create_response

router = APIRouter(tags=["public"])


@router.get("/ping")
async def ping():
    return create_response(message="pong")
