from typing import Optional
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from core.security import get_password_hash, create_access_token, authenticate_user
from models.auth_models import Users
from core.secure_logger import get_logger

logger = get_logger("auth_services")


def get_user_by_id(db: Session, user_id: str) -> Optional[Users]:
    try:
        return db.query(Users).filter(Users.user_id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to get user at this time"
        )


def create_token(db: Session, user: Users, expires_delta: Optional[timedelta] = None) -> str:
    token = create_access_token(user.username, user.user_id, expires_delta)
    user.token = token
    try:
        db.add(user)
        db.commit()
        logger.info(f"Token created for user: {user.user_id}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create token"
        )
    return token


def logout_user(db: Session, user_id: str) -> bool:
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"User not found for logout: {user_id}")
            return False
        
        # FIX: token is a string, not a list. Changed .remove() to = None
        user.token = None
        db.add(user)
        db.commit()
        logger.info(f"User logged out successfully: {user_id}")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error logging out user: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during logout: {str(e)}")
        return False
