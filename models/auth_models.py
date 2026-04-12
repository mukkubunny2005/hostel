from sqlalchemy import Column, String, Boolean
from database.database import Base

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "hostel_management"}
    user_id = Column(String(200), primary_key=True)
    hostel_id = Column(String(200), unique=True)
    user_role = Column(String(20))
    hostel_name = Column(String(100))
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    token = Column(String(300))
    is_active = Column(Boolean, default=True)
