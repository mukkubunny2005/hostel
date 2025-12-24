from sqlalchemy.orm import Session

from core.security import get_password_hash
from models.hostel_registration_models import *
from schemas.hostel_registration_schemas import *


def create_hostel(db: Session, hostel_request: HostelRequest) -> Hostel:
    hostel_form = Hostel(
        **hostel_request.model_dump(),
        password=get_password_hash(hostel_request.password),
    )
    db.add(hostel_form)
    db.commit()
    db.refresh(hostel_form)

    menu = Menu(
        **hostel_request.model_dump(),
        hostel_id = hostel_form.id

    )
    db.add(menu)
    db.commit()
    db.refresh(menu)

    wifi = WifiScreens(
        **hostel_request.model_dump(),
        hostel_id = hostel_form.id
    )
    db.add(wifi)
    db.commit()
    db.refresh(wifi)

    return hostel_form
