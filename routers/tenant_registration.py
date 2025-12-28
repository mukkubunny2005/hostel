from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import tenant_registration_Services as tenant_services
from models.tenant_registration_models import *
from database.session import get_db
from typing import Annotated
router = APIRouter()
import uuid
from sqlalchemy.exc import SQLAlchemyError
from core.security import *


@router.post('/tenant_registration', response_model=TenantCreate)
async def tenant_registration_form(db: Annotated[Session, Depends(get_db)], hostel_id:str, user_id:str):
    try:
        tenant_form = tenant_services.create_tenant(db, user_id, uuid, hostel_id)
        
        return {"message": "Tenant created", "tenant_id": uuid, "hostel_id":hostel_id}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user at this time"
        )



