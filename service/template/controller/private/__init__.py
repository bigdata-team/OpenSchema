from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from common.model.http import create_response


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(tags=["private"], dependencies=[Depends(oauth2_scheme)])


@router.get("/ping")
async def ping():
    return create_response()
