from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Depends

DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5433/hostel_management"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
load_dotenv()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
