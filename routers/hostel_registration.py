import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.session import get_db
from models.hostel_registration_models import HostelRegistrationRequest
from services import hostel_registration_services as hostel_services

router = APIRouter()


@router.post('/', response_model=HostelRegistrationRequest,
    status_code=status.HTTP_201_CREATED)
def hostel_registration_from(db: Annotated[Session, Depends(get_db)], hostel_id: uuid.uuid5, owner_id: str, hostels:str = bool):
    owner_id_ = owner_id if hostels and owner_id else str(uuid.uuid4())
    try:
        hostel_form = hostel_services.create_hostel(db=db, hostel_id=hostel_id, owner_id=owner_id_)
        return {"msg": "hostel created", "hostel_id": hostel_form.hostel_id, "owner_id" : hostel_form.owner_id}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user at this time"
        )
