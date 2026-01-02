import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.trace_id = str(uuid.uuid5())
        response = await call_next(request)
        response.headers["X-Trace-ID"] = request.state.trace_id
        return response
