from datetime import datetime, timedelta, timezone
from typing import Optional
from typing import Annotated

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database_pkg.session import get_db
from schemas.auth_schemas import Users
from pwdlib import PasswordHash

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")
password_hash = PasswordHash.recommended()

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


def create_access_token(subject: str, user_id: str, expires_delta: timedelta) -> str:
    to_encode = {"sub": subject, "id": user_id}
    if expires_delta :
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)


async def get_current_user(token: Annotated[str, security(oauth2_bearer)]) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'www-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_role: str = payload.get('role')
        user_id: str = payload.get("id")

        if username is None or user_id is None:
            raise credentials_exception
        
        return {"username": username, "id": user_id, "user_role" : user_role}
    except JWTError:
        raise credentials_exception

async def get_current_active_user(current_user : dict = Annotated[Users, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='inactive user')
    return current_user

