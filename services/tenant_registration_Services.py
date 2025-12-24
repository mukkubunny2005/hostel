from sqlalchemy.orm import Session
from models.tenant_registration_models import *
from settings.dependencies import *
from schemas.tenant_Registration_schemas import (
    TenantRegistration,
    TenantStudent,
    TenantEmployee,
    TenantSelfEmployed,
    TenantOther,
)

async def create_tenant(db: Session, tenant_create:TenantCreate, uuid, hostel_id:str, tenant_id:str) -> TenantRegistration:
    
    tenant = TenantRegistration(
        **tenant_create.model_dump(),
        govt_id_file=await tenant_create.govt_id_file.read(),
        tenant_id = tenant_id,
        hostel_id = hostel_id
    ),
    
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    tenant_necessity = db.query(TenantRegistration).filter(TenantRegistration.hostel_id == hostel_id).filter(TenantRegistration.tenant_id == tenant_id).first()
    if not tenant_necessity:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    match tenant_necessity.necessity:
            case NecessityEnum.Student:
                add_student_details(db, uuid, hostel_id, tenant_id)
            case NecessityEnum.Employee:
                add_employee_details(db,uuid, hostel_id, tenant_id)
            case NecessityEnum.SelfEmployment:
                add_self_employed(db, uuid , hostel_id, tenant_id)
            case NecessityEnum.Other:
                add_other(db,uuid, hostel_id, tenant_id)
    return tenant


async def add_student_details(db: Session, tenant_student_create:TenantStudentCreate) -> TenantStudent:
    student = TenantStudent(
        **tenant_student_create.model_dump(),
        id_card_photo=await tenant_student_create.id_card_photo.read(),
        tenant_id = tenant_student_create.tenant_id,
        hostel_id = tenant_student_create.hostel_id
    )
    db.add(student)
    db.commit()
   
    return student


async def add_employee_details(db: Session, tenant_employee_create:TenantEmployeeCreate, tenant_id:str, hostel_id:str) -> TenantEmployee:
    employee = TenantEmployee(
        **tenant_employee_create.model_dump(),
        id_card_image=await tenant_employee_create.id_card_image.read(),
        hostel_id = hostel_id,
        tenant_id = tenant_id
    )
    db.add(employee)
    db.commit()
    
    return employee


def add_self_employed(db: Session, tenant_Self_employee_create:TenantSelfEmployedCreate) -> TenantSelfEmployed:
    self_emp = TenantSelfEmployed(
        **tenant_Self_employee_create.model_dump(),
        govt_id_proof = tenant_Self_employee_create.govt_id_proof.read()
    )
    db.add(self_emp)
    db.commit()
    return self_emp


def add_other(db: Session, tenant_other_create:TenantOtherCreate) -> TenantOther:
    other = TenantOther(
        **tenant_other_create.model_dump(),
        govt_id_proof = tenant_other_create.govt_id_proof.read(),
        tenant_id=tenant_other_create.tenant_id,
    )
    db.add(other)
    db.commit()
   
    return other

