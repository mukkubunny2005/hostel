from sqlalchemy import Column, String, Boolean
from database_pkg.database import Base3

import uuid

class Users(Base3):
    __tablename__ = 'authentication'
    id = Column(String(200), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    first_name = Column(String(200))
    last_name = Column(String(200))
    email = Column(String(100))
    username = Column(String(100), nullable=False, unique=True)
    ph_no = Column(String(50))
    password = Column(String(300), nullable=False)
    token = Column(String(300))
    is_active = Column(Boolean, default=True)

