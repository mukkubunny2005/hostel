from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from typing import Annotated
from models.hostel_registration_models import *
from schemas.tenant_Registration_schemas import *
from models.hostel_registration_models import *
import uuid
from sqlalchemy.exc import SQLAlchemyError

from services import hostel_registration_services as hostel_services
from schemas.auth_schemas import *
router = APIRouter()

@router.post('/', response_model=HostelRequest,
    status_code=status.HTTP_201_CREATED)
def hostel_registration_from(db: Annotated[Session, Depends(get_db)], uuid: uuid.uuid4):
    try:
        hostel_form = hostel_services.create_hostel(db, uuid)
        return {"msg": "hostel created", "hostel_id": uuid}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user at this time"
        )


    


