from starlette.middleware.base import BaseHTTPMiddleware
from .jwt import JWTService
from uuid import uuid4
from fastapi.exceptions import HTTPException


class TransactionIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        header = "X-Transaction-Id"
        txid = request.headers.get(header)
        if not txid:
            txid = str(uuid4())
        request.state.txid = txid

        response = await call_next(request)
        response.headers[header] = txid
        return response
