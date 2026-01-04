from sqlalchemy.orm import Session
from core.security import get_password_hash
from models.hostel_registration_models import *
from schemas.hostel_registration_schemas import *
from schemas.auth_schemas import Users

def create_hostel(db: Session, hostel_request: HostelRegistrationRequest, hostel_id:str, owner_id:str) -> HostelRegistration:
    hostel_form = HostelRegistration(
        **hostel_request.model_dump(),
        hostel_id = hostel_id,
        password=get_password_hash(hostel_request.password),
        owner_id = owner_id
    )
    
    user = Users(**hostel_request.model_dump, password = get_password_hash(hostel_request.password),
                 user_role = 'owner', hostel_id = hostel_id, user_id = owner_id
                 )

    db.add(hostel_form)
    db.add(user)
    db.commit()
    db.refresh(hostel_form)
    db.refresh(user)

    menu = Menu(
        **hostel_request.model_dump(),
        hostel_id = hostel_form.hostel_id

    )
    db.add(menu)
    db.commit()
    db.refresh(menu)

    wifi = WifiScreens(
        **hostel_request.model_dump(),
        hostel_id = hostel_form.hostel_id
    )
    db.add(wifi)
    db.commit()
    db.refresh(wifi)
    return hostel_form

