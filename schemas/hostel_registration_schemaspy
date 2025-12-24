from sqlalchemy import Column, Integer, String, Boolean, Enum, DECIMAL, ForeignKey, LargeBinary, Date
from database.database import Base
import enum

class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"

class Hostel(Base):
    __tablename__ = "hostels"
    __table_args__ = {"schema": "hostel_form"}
    id = Column(String(225), primary_key=True)
    hostel_name = Column(String(225), nullable=False)
    area = Column(String(225), nullable=False)
    city = Column(String(225), nullable=False)
    state = Column(String(225), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    phone_number = Column(String(20), nullable=False)

    veg = Column(Boolean, default=False)
    non_veg = Column(Boolean, default=False)

    ac = Column(Boolean, default=False)
    non_ac = Column(Boolean, default=False)

    no_of_ac_beds = Column(Integer, default=0)
    no_of_non_ac_beds = Column(Integer, default=0)

    non_ac_sharing = Column(Boolean, default=False)
    non_ac_sharing_price = Column(DECIMAL(10,2), default=0.00)

    ac_sharing = Column(Boolean, default=False)
    ac_sharing_price = Column(DECIMAL(10,2), default=0.00)
    username = Column(String(100), unique=True)
    password = Column(String(500))

    terms_and_conditions = Column(String(500))
    rules_and_regulations = Column(String(500))

class Menu(Base):
    __tablename__ = 'menu'
    __table_args__ = {"schema": "hostel_form"}
    id = Column(String(225), ForeignKey('hostel_form.hostels.id'), primary_key=True)
    monday = Column(String(50))
    tuesday = Column(String(50))
    wednesday = Column(String(50))
    thursday = Column(String(50))
    friday = Column(String(50))
    saturday = Column(String(50))
    sunday = Column(String(50))


class WifiScreens(Base):
    __tablename__ = 'wifiscreens'
    __table_args__ = {"schema": "hostel_form"}
    id = Column(String(225), ForeignKey('hostel_form.hostels.id'), primary_key=True)

    screens = Column(String(50))
    password = Column(String(50))