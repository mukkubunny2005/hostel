from typing import Generator
from sqlalchemy.orm import Session
from database_pkg.database import SessionLocal, SessionLocal2, SessionLocal3
from typing import Annotated
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
