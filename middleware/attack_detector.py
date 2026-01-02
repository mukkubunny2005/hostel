from fastapi import Request, HTTPException, status
from collections import defaultdict
import time
FAILED_ATTEMPTS = defaultdict(list)
MAX_ATTEMPTS = 5
BLOCK_TIME = 900
async def detect_attack(request:Request):
    ip = request.client.host
    now = time.time()
    FAILED_ATTEMPTS[ip] = [t for t in FAILED_ATTEMPTS[ip] if now - t < BLOCK_TIME]
    if len(FAILED_ATTEMPTS[ip]) >= MAX_ATTEMPTS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="IP temporarily blocked")
    FAILED_ATTEMPTS[ip].append(now)
    
    