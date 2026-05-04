import datetime

from fastapi import Depends, Form, UploadFile
from pydantic import BaseModel, Field

from models.enums import FoodEnum, GenderEnum, GovtIDEnum, NecessityEnum, RoomEnum
from settings.dependencies import validate_file_security


class TenantCreate(BaseModel):
    tenant_id: str = Form(...)
    first_name: str = Form(min_length=1, max_length=20)
    last_name: str = Form(min_length=1, max_length=20)

    user_name: str = Form(..., min_length=5, max_length=200)
    password: str = Form(min_length=6)
    
    phone_number: str = Form(min_length=10, max_length=15)
    father_name: str = Form(min_length=1, max_length=200)
    father_phone_number: str = Form(max_length=15)
    gender: GenderEnum = Form(...)
    date_of_birth: datetime.date = Form(...)
    address: str = Form(min_length=5, max_length=1000)
    house_no: str = Form(min_length=1, max_length=50)
    street: str = Form(min_length=1, max_length=200)
    colony: str = Form(min_length=1, max_length=200)
    landmark: str = Form(min_length=0, max_length=200)
    city: str = Form(min_length=1, max_length=100)
    state: str = Form(min_length=1, max_length=100)
    pincode: str = Form(min_length=4, max_length=12)
    country: str = Form("India", min_length=2, max_length=100)
    govt_id_type: GovtIDEnum = Form(...)
    govt_id_number: str = Form(min_length=4, max_length=100)
    
    emergency_contact: str = Form(min_length=7, max_length=15)
    food_preference: FoodEnum = Form(...)
    room_type: RoomEnum = Form(...)

    govt_id_file: UploadFile = Depends(validate_file_security)
    
    necessity: NecessityEnum = Form(...)
    model_config = {
        "str_strip_whitespace": True,   
        "extra": "allow",         
        "from_attributes": True,     
    }

class TenantStudentCreate(BaseModel):
    hostel_id: str = Form(...)
    tenant_id: str = Form(...)
    studying_at: str = Form(...)
    student_id_number: str = Form(...)
    college_address: str = Form(...)
    city: str = Form(...)
    pincode: str = Form(...)
    phone_number: str = Form(min_length=10, max_length=15)
    id_card_photo: UploadFile = Depends(validate_file_security)
    model_config = {
        "str_strip_whitespace": True,   
        "extra": "allow",         
        "from_attributes": True, 
    }


class TenantEmployeeCreate(BaseModel):
    tenant_id: str = Form(...)
    company_name: str = Form(...)
    employee_id_number: str = Form(...)
    address: str = Form(...)
    city: str = Form(...)
    pincode: str = Form(...)
    phone_number: str = Form(min_length=10, max_length=15)
    id_card_image: UploadFile = Depends(validate_file_security)
    model_config = {
        "str_strip_whitespace": True,   
        "extra": "allow",         
        "from_attributes": True,     
    }

class TenantSelfEmployedCreate(BaseModel):
    tenant_id: str = Form(...)
    occupation: str = Form(...)
    phone_number: str = Form(min_length=10, max_length=15)
    govt_id_proof: UploadFile = Depends(validate_file_security)
    model_config = {
        "str_strip_whitespace": True,   
        "extra": "allow",           
        "from_attributes": True         
    }

class TenantOtherCreate(BaseModel):
    tenant_id: str = Form(...)
    description: str = Form(...)
    phone_number: str = Form(min_length=10, max_length=15)
    govt_id_proof: UploadFile = Depends(validate_file_security)
    model_config = {
        "str_strip_whitespace": True,   
        "extra": "allow",         
        "from_attributes": True         
    }
