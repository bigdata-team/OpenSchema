from __future__ import annotations

import re
from typing import Callable, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from common.jwt import verify_token
from starlette.responses import Response
from pathlib import Path
from common.model.http import create_response


def _get_bearer_token(value: str, prefix: str = "Bearer ") -> Optional[str]:
    v = (value or "").strip()
    if not v:
        return None
    if not v.startswith(prefix):
        return None
    token = v[len(prefix) :].strip()
    return token or None


class AuthenticationMiddleware(BaseHTTPMiddleware):
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
        header = request.headers.get(self.auth_header, "")
        token = _get_bearer_token(header, self.token_prefix)
        payload = verify_token(
            token,
            issuer=self.issuer,
            audience=self.audience,
        )
        request.state.token = token
        request.state.token_payload = payload
        for pattern in self.bypass_patterns:
            if pattern.match(request.url.path):
                response = await call_next(request)
                return response

        if not payload:
            return create_response("Unauthorized", code=401)
        response = await call_next(request)
        return response
