from typing import Optional
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from core.security import get_password_hash, create_access_token, authenticate_user
from schemas.auth_schemas import Users

# async def create_user(db: Session, email: str, username: str, first_name: Optional[str], last_name: Optional[str], password: str, ph_no: Optional[str]) -> Users:
#     existing_user = db.query(Users).filter(Users.username == username).first()
#     if existing_user:
#         return None
#     try:
#         user_model = Users(
#             email=email,
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             password=get_password_hash(password),
#             ph_no=ph_no,
#             is_active=True,
#         )
#         db.add(user_model)
#         db.commit()
#         db.refresh(user_model)
#         return user_model
#     except SQLAlchemyError:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Unable to create user at this time"
#         )
    


def get_user_by_id(db: Session, hostel_id:str) -> Users:
    try:
        return db.query(Users).filter(Users.hostel_id == hostel_id).filter().first()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get user at this time"
        )



def create_token(db: Session, user: Users, expires_delta: Optional[timedelta] = None) -> str:
    token = create_access_token(user.username, user.id, expires_delta)
    user.token = token
    db.add(user)
    db.commit()
    return token


def change_password(db: Session, user_id: str, current_password: str, new_password: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    auth = authenticate_user(db, user.username, current_password)
    if not auth:
        return False
    user.password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    return True


def logout_user(db: Session, user_id: str) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.token.remove()
    db.add(user)
    db.commit()
    return True
