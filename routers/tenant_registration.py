from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import tenant_registration_Services as tenant_services
from models.tenant_Registration_models import *
from database.session import get_db
from typing import Annotated
router = APIRouter()
import uuid
from sqlalchemy.exc import SQLAlchemyError
from core.security import *
from auth import db_dependency
from owner import *
@router.post('/tenant_registration', response_model=TenantCreate)
async def tenant_registration_form(db: Annotated[Session, Depends(get_db)], hostel_id:str , tenant_id:str = uuid.uuid5):
    try:
        tenant_form = tenant_services.create_tenant(db=db, tenant_id=tenant_id, hostel_id=hostel_id)
        return {"message": "Tenant created", "tenant_id": tenant_id, "hostel_id":hostel_id}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user at this time"
        )

@router.get('/particular_hostel/{hostel_id}')
def particular_hostel(hostel_id:str, db:db_dependency, current_user:user_dependency):
    db_dependency