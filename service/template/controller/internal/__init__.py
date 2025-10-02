from fastapi import APIRouter
from common.model.http import create_response

router = APIRouter(tags=["internal"])


@router.get("/ping")
async def ping():
    return create_response()
