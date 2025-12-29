from datetime import datetime, timedelta, timezone
from typing import Optional
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, security, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.audit_logger import get_audit_logger
from core.secure_logger import get_logger
from middleware.attack_detector import detect_attack

from schemas.auth_schemas import Users
from pwdlib import PasswordHash

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")
password_hash = PasswordHash.recommended()
logger = get_logger("security")
SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'RS256'

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> Users:
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(subject: str, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": subject, "user_id": user_id}
    audit_logger = get_audit_logger()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)

    audit_logger.warning(f"Created access token: subject={subject}, user_id={user_id}, exp={expire.isoformat()}")
    to_encode.update({"exp": expire})
    audit_logger.warning(f'token updated with : {expire}')
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, security(oauth2_bearer)], request: Request) -> dict:
    await detect_attack(request)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'www-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_role: str = payload.get('role')
        user_id: str = payload.get("user_id")
        hostel_id: str = payload.get('hostel_id')

        if username is None or user_id is None or hostel_id is None:
            logger.warning('could not get user')
            raise credentials_exception
        
        return {"username": username, "id": user_id, "user_role" : user_role}
    except JWTError as e:
        logger.error(e)
        raise credentials_exception

async def get_current_active_user(current_user : dict = Annotated[Users, Depends(get_current_user)]):
    if current_user is None:
        logger.error('unable to get user')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='inactive user')
    return current_user
