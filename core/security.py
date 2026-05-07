from datetime import datetime, timedelta, timezone
from typing import Optional
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.secure_logger import get_logger
from middleware.attack_detector import detect_attack
import os
from dotenv import load_dotenv

load_dotenv()

from schemas.auth_schemas import Users
from pwdlib import PasswordHash

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")
password_hash = PasswordHash.recommended()


if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set. Please set it in .env file")

from core.config import settings

settings.SECRET_KEY

# Initialize logger
logger = get_logger("security")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[Users]:
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(subject: str, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": subject, "user_id": user_id}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)

    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# FIX 2: Async function with proper error handling and logging
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], request: Request) -> dict:
    await detect_attack(request)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'}  # FIX: Fixed header name from 'www-Authenticate' to 'WWW-Authenticate'
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_role: str = payload.get('role')
        user_id: str = payload.get("user_id")
        hostel_id: str = payload.get('hostel_id')

        if username is None or user_id is None:
            logger.warning('Could not extract required claims from token')
            raise credentials_exception
        
        logger.info(f'User {username} authenticated successfully')
        return {"username": username, "id": user_id, "user_role": user_role, "hostel_id": hostel_id}
    except JWTError as e:
        logger.error(f'JWT validation error: {str(e)}')
        raise credentials_exception

async def get_current_active_user(current_user: dict = Annotated[dict, Depends(get_current_user)]) -> dict:
    if current_user is None:
        logger.error('Could not retrieve user from token')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is inactive or not found')
    return current_user
