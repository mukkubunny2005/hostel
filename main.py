from fastapi import FastAPI, Request
from middleware.request_trace import RequestTraceMiddleware
from routers import tenant_registration, hostel_registration, auth, owner
from database.database import Base, engine
import time
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestTraceMiddleware)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

app.include_router(hostel_registration.router)
app.include_router(tenant_registration.router)
app.include_router(auth.router)
app.include_router(owner.router)