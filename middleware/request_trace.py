import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class RequestTraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.trace_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Trace-ID"] = request.state.trace_id
        return response
