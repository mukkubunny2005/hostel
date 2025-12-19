from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from database_pkg.session import get_db
from models.hostel_registration_models import GenderEnum
from models.tenant_Registration_models import GovtIDEnum, NecessityEnum, FoodEnum, RoomEnum
from services import tenant_registration_Services as tenant_services
from schemas.tenant_registration_schemas import *
from typing import Annotated
router = APIRouter()
import uuid
from sqlalchemy.exc import SQLAlchemyError
from services.auth_services import *
from services.tenant_registration_Services import *
from models.auth_models import *
from services.hostel_registration_services import *
from core.security import *





@router.post('/tenant_registration', response_model=TenantCreate)
async def tenant_registration_form(db: Annotated[Session, Depends(get_db)], uuid: uuid.uuid4, user:Annotated[Users, Depends(get_current_user)], hostel_id:str):
    try:
        if user is None:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
                )
        tenant_form = tenant_services.create_tenant(db, user.id, uuid, hostel_id)
        
        
        return {"message": "Tenant created", "tenant_id": uuid}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user at this time"
        )
    



