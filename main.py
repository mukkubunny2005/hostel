from fastapi import FastAPI, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from middleware.request_trace import TraceMiddleware
from routers import tenant_registration, hostel_registration, auth
from database.database import Base, engine
import time


app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TraceMiddleware)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
	start_time = time.perf_counter()
	response = await call_next(request)
	process_time = time.perf_counter() - start_time
	response.headers['X-Process-Time'] = str(process_time)
	return response


@app.get('/startup_event')
async def startup_event():
	Base.metadata.create_all(bind=engine)
	

app.include_router(hostel_registration.router)
app.include_router(tenant_registration.router)
app.include_router(auth.router)


