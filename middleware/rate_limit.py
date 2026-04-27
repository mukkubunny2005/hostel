from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time

# Simple in-memory store (use Redis in production)
REQUEST_LOG = {}

RATE_LIMIT = 5   # requests
WINDOW = 10      # seconds

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        if client_ip not in REQUEST_LOG:
            REQUEST_LOG[client_ip] = []

        # Remove old requests
        REQUEST_LOG[client_ip] = [t for t in REQUEST_LOG[client_ip] if now - t < WINDOW]

        if len(REQUEST_LOG[client_ip]) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests")

        REQUEST_LOG[client_ip].append(now)

        response = await call_next(request)
        return response
