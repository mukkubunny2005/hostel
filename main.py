from contextlib import asynccontextmanager
import time
from typing import AsyncIterator, List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine
from middleware.secure_middleware import SecureMiddleware
from middleware.rate_limit import RateLimitMiddleware
from routers import tenant_registration, hostel_registration, auth, owner


# Configure allowed frontend origins here instead of "*"
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:8000",
    # "https://your-frontend-domain.com",
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan context.

    Use Alembic for production migrations; this is fine for local/dev.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


# Middleware registration
app.add_middleware(SecureMiddleware)       # Fail fast on security issues
app.add_middleware(RateLimitMiddleware)    # Enforce rate limits
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Measure request processing time and expose it in X-Process-Time header.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    # Limit precision to keep headers small and readable
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response


# Routers
app.include_router(hostel_registration.router)
app.include_router(tenant_registration.router)
app.include_router(auth.router)
app.include_router(owner.router)
