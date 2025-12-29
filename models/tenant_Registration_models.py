from pydantic import BaseModel
from fastapi import APIRouter, Depends, UploadFile, File, Form, Path
import datetime
from typing import Optional
from schemas.tenant_Registration_schemas import *
import os
from settings.dependencies import *

class TenantCreate(BaseModel):
    tenant_id : str = Form(...,)
    first_name: str = Form(..., min_length=1, max_length=200),
    last_name: str = Form(..., min_length=1, max_length=200),

    user_name: str = Form(...,min_length=5, max_length=200),
    password: str = Form(..., min_length=6)
    
    phone_number: int = Form(..., min_length=10),
    father_name: str = Form(..., min_length=1, max_length=200),
    father_phone_number: str = Form(..., max_length=10),
    gender: GenderEnum = Form(...),
    date_of_birth: datetime.date = Form(...),
    address: str = Form(..., min_length=5, max_length=1000),
    house_no: str = Form(..., min_length=1, max_length=50),
    street: str = Form(..., min_length=1, max_length=200),
    colony: str = Form(..., min_length=1, max_length=200),
    landmark: str = Form(..., min_length=0, max_length=200),
    city: str = Form(..., min_length=1, max_length=100),
    state: str = Form(..., min_length=1, max_length=100),
    pincode: str = Form(..., min_length=4, max_length=12),
    country: str = Form("India", min_length=2, max_length=100),
    govt_id_type: GovtIDEnum = Form(...),
    govt_id_number: str = Form(..., min_length=4, max_length=100),
    
    emergency_contact: str = Form(..., min_length=7, max_length=15),
    food_preference: FoodEnum = Form(...),
    room_type: RoomEnum = Form(...),

    govt_id_file: UploadFile = Depends(validate_file_security),
    
    necessity: NecessityEnum = Form(...,),

class TenantStudentCreate(BaseModel, Form):
    hostel_id: str 
    tenant_id: str
    studying_at: str
    student_id_number: str
    college_address: str
    city: str
    pincode: str
    phone_number: str
    id_card_photo: UploadFile = Depends(validate_file_security),
    class Config:
        anystr_strip_whitespace = True
        extra = "forbid"
        orm_mode = True


class TenantEmployeeCreate(BaseModel, Form):
    tenant_id: str
    company_name: str
    employee_id_number: str
    address: str
    city: str
    pincode: str
    phone_number: str
    id_card_image: UploadFile = Depends(validate_file_security),
    class Config:
        anystr_strip_whitespace = True
        extra = "forbid"
        orm_mode = True

class TenantSelfEmployedCreate(BaseModel, Form):
    tenant_id: str
    occupation: str
    phone_number: int = Path(lt=10)
    govt_id_proof: UploadFile = Depends(validate_file_security)
    class Config:
        anystr_strip_whitespace = True
        extra = "forbid"
        orm_mode = True

class TenantOtherCreate(BaseModel, Form):
    tenant_id: str
    description: str
    phone_number: int = Path(lt=10)
    govt_id_proof: UploadFile = Depends(validate_file_security)
    class Config:
        anystr_strip_whitespace = True
        extra = "forbid"
        orm_mode = True