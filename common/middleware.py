from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
from fastapi.exceptions import HTTPException
from common.jwt import (
    get_tokens,
    verify_access_token,
    verify_access_token_now,
    decode,
    TokenPayload,
)
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from functools import wraps


import os
from fastapi import Request


class XTransactionIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        header = "X-Transaction-Id"
        txid = request.headers.get(header)
        if not txid:
            txid = str(uuid4())
        request.state.txid = txid

        response = await call_next(request)
        response.headers[header] = txid
        return response


class XServiceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        header = "X-Service-Id"
        response = await call_next(request)
        response.headers[header] = os.getenv("SERVICE_ID")
        return response


class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        request.state.tokens = get_tokens(request)
        response = await call_next(request)
        return response


def identify(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        if not request:
            request = kwargs.get("request")

        if not request or not hasattr(request, "state"):
            raise HTTPException(status_code=400, detail="Request object not found")

        tokens = get_tokens(request)
        access_token = tokens.get("cookie_access_token") or tokens.get("bearer_token")
        try:
            payload = TokenPayload(**decode(access_token, "auth.service", "service"))
        except:
            payload = TokenPayload(sub=None, sid=None, iat=None, exp=None, jti=None)
        request.state.token = payload
        return await func(*args, **kwargs)


# decorator
def protected(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        if not request:
            request = kwargs.get("request")

        if not request or not hasattr(request, "state"):
            raise HTTPException(status_code=400, detail="Request object not found")

        tokens = get_tokens(request)
        access_token = tokens.get("cookie_access_token") or tokens.get("bearer_token")
        payload = verify_access_token(access_token)
        request.state.token = payload
        return await func(*args, **kwargs)

    return wrapper


def blprotected(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        if not request:
            request = kwargs.get("request")

        if not request or not hasattr(request, "state"):
            raise HTTPException(status_code=400, detail="Request object not found")

        tokens = get_tokens(request)
        access_token = tokens.get("cookie_access_token") or tokens.get("bearer_token")
        payload = await verify_access_token_now(access_token)
        request.state.token = payload
        return await func(*args, **kwargs)

    return wrapper


# class JWTMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request, call_next):
#         tokens = get_tokens(request)
#         access_token = (
#             tokens.get("cookie_access_token") or tokens.get("bearer_token") or None
#         )

#         payload = verify_access_token(access_token)
#         request.state.token = payload

#         response = await call_next(request)
#         return response
