import re

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from common.model.http import create_response_model
from common.util.jwt import verify_token


def _get_bearer_token(value: str, prefix: str = "Bearer ") -> str | None:
    v = (value or "").strip()
    if not v:
        return None
    if not v.startswith(prefix):
        return None
    token = v[len(prefix) :].strip()
    return token or None


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        auth_header: str = "Authorization",
        token_prefix: str = "Bearer ",
        issuer: str = "auth.service",
        audience: str = "service",
        bypass_patterns: list[str] = [
            r".*/docs.*",
            r".*/redoc.*",
            r".*/openapi\.json$",
            r".*/ping.*$",
            r".*/healthz.*$",
        ],
    ) -> None:
        super().__init__(app)
        self.auth_header = auth_header
        self.token_prefix = token_prefix
        self.issuer = issuer
        self.audience = audience
        self.bypass_patterns = [re.compile(pattern) for pattern in bypass_patterns]

    async def dispatch(self, request: Request, call_next: callable):
        for pattern in self.bypass_patterns:
            if pattern.match(request.url.path):
                response = await call_next(request)
                return response

        header = request.headers.get(self.auth_header, "")
        token = _get_bearer_token(header, self.token_prefix)
        payload = verify_token(token, issuer=self.issuer, audience=self.audience)
        request.state.token = token
        request.state.token_payload = payload

        if not payload:
            raise HTTPException(
                status_code=401,
                detail=create_response_model(
                    message="Unauthorized", detail="Invalid token"
                ),
            )
        response = await call_next(request)
        return response


def get_require_auth(
    *,
    auth_header: str = "Authorization",
    token_prefix: str = "Bearer ",
    issuer: str = "auth.service",
    audience: str = "service",
):
    def dependency(request: Request):
        header = request.headers.get(auth_header, "")
        token = _get_bearer_token(header, token_prefix)
        payload = verify_token(token, issuer=issuer, audience=audience)
        request.state.token = token
        request.state.token_payload = payload

        if not payload:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
            )
        return payload

    return dependency
