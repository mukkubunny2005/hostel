from sqlalchemy import Column, String, Enum, ForeignKey, LargeBinary, Date, Integer
from database.database import Base
from models.all_enums import GenderEnum, FoodEnum, GovtIDEnum, NecessityEnum, RoomEnum

class TenantRegistration(Base):
    __tablename__ = "tenant_registration"
    __table_args__ = {"schema": "public"}
    hostel_id = Column(String(225), unique=True, primary_key=True)
    tenant_id = Column(String(225), primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    phone_number = Column(Integer(), nullable=False)
    father_name = Column(String(50))
    father_phone_number = Column(Integer())
    gender = Column(Enum(GenderEnum), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String(100))
    house_no = Column(String(50))
    street = Column(String(50))
    colony = Column(String(50))
    landmark = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    pincode = Column(String(20))
    country = Column(String(20), default="India")
    govt_id_type = Column(Enum(GovtIDEnum), nullable=False)
    govt_id_file = Column(LargeBinary, nullable=True)
    govt_id_number = Column(String(50), nullable=False)
    necessity = Column(Enum(NecessityEnum), nullable=False)
    emergency_contact = Column(String(15))
    food_preference = Column(Enum(FoodEnum), nullable=False)
    room_type = Column(Enum(RoomEnum), nullable=False)

class TenantStudent(Base):
    __tablename__ = "tenant_student"
    __table_args__ = {"schema": "public"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id"), primary_key=True)
    studying_at = Column(String(200), nullable=False)
    student_id_number = Column(String(50), nullable=False)
    id_card_photo = Column(LargeBinary)
    college_address = Column(String(50))
    city = Column(String(100))
    pincode = Column(String(10))
  
class TenantEmployee(Base):
    __tablename__ = "tenant_employee"
    __table_args__ = {"schema": "public"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id", ondelete="CASCADE"), primary_key=True)
    company_name = Column(String(200), nullable=False)
    employee_id_number = Column(String(50), nullable=False)
    id_card_image = Column(LargeBinary)
    address = Column(String(50))
    city = Column(String(100))
    pincode = Column(String(10))

   

class TenantSelfEmployed(Base):
    __tablename__ = "tenant_self_employed"
    __table_args__ = {"schema": "public"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id", ondelete="CASCADE"), primary_key=True)
    occupation = Column(String(200), nullable=False)
    

class TenantOther(Base):
    __tablename__ = "tenant_other"
    __table_args__ = {"schema": "public"}
    tenant_id = Column(String(225), ForeignKey("tenant.tenant_registration_form.tenant_id", ondelete="CASCADE"), primary_key=True)
    description = Column(String(500))

    