from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from common.util.random import get_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        header: str = "X-Correlation-Id",
        state_key: str = "crid",
    ) -> None:
        super().__init__(app)
        self.header = header
        self.state_key = state_key

    async def dispatch(self, request: Request, call_next: callable):
        crid = request.headers.get(self.header, "").strip()
        crid = crid or get_id()
        setattr(request.state, self.state_key, crid)

        response = await call_next(request)
        response.headers[self.header] = crid
        return response
