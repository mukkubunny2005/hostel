from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
from database.session import get_db
from core.security import (
    authenticate_user,
    get_current_user,
    oauth2_bearer,
)
from models.auth_models import UserCreate, Token, UserVerification, UserOut
from schemas.auth_schemas import Users
from services import auth_services as auth_services


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/get_user", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user( db: db_dependency, current: Annotated[Users, Depends(get_current_user)]):
    if current is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    try:
        user = auth_services.get_user_by_id(db, current.get("id"))
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[str, Depends(get_db)]):
    created = auth_services.create_user(
        db,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        ph_no=user.ph_no,
    )
    if created is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"msg": "User created successfully", "user_id": created.id}


@router.post("/token", response_model=Token)
async def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends(), ) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"www-Authenticate": "Baarer"})
    token = auth_services.create_token(db, user, timedelta(minutes=20))
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "user_id": user.id,
    }


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    db: db_dependency, 
    user_verification: UserVerification,
    current: dict = Depends(get_current_user),
):

    if current is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    ok = auth_services.change_password(db, current.get("id"), user_verification.password, user_verification.new_password)
    if not ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect current password or user not found")
    return {"msg": "password changed successfully"}


@router.delete('/logout')
async def logout(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_bearer),
):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    user = auth_services.get_user_by_id(db, current_user.get('id'))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not user.token or user.token != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token or already logged out')

    logout = auth_services.logout_user(db, user.id)
    if not logout:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to logout user")
    return {'msg': 'user logged out successfully'}
