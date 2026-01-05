from fastapi import APIRouter ,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from database.session import get_db
from core.secure_logger import get_logger
from middleware.attack_detector import detect_attack
from auth import detect_attack, db_dependency
from models.tenant_registration_models import *
from models.hostel_registration_models import *
from models.auth_models import *
from schemas.auth_schemas import *
from schemas.hostel_registration_schemas import *
from schemas.tenant_registration_schemas import *
from core.security import (
    authenticate_user,
    get_current_user,
    oauth2_bearer,
    bcrypt_context,
    get_password_hash
)
router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]

router.get('/get_tenant/{hostel_id}/{tenant_id}', status_code=status.HTTP_204_NO_CONTENT)
async def get_hostel_tenants(db: db_dependency, current_user:user_dependency):
    detect_attack()
    if current_user is None or current_user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    user = db.query(Users).filter(Users.user_id == current_user.get('user_id')).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    tenants = db.query(HostelRegistration).filter(HostelRegistration.hostel_id == user.hostel_id).filter(HostelRegistration.owner_id == current_user.get('user_id')).filter()
    if tenants is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    return tenants

router.delete('/delete_tenant/{hostel_id}/{tenant_id}')
async def delete_tenant(db: db_dependency, current_user:user_dependency, tenant_id:str):
    detect_attack()
    if current_user is None or current_user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    user = db.query(Users).filter(Users.user_id == current_user.get('user_id')).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    tenants = db.query(TenantRegistration).filter(TenantRegistration.hostel_id == user.hostel_id).filter(HostelRegistration.owner_id == current_user.get('user_id')).filter(TenantRegistration.tenant_id == tenant_id).first()
    user_tenant = db.query(Users).filter(Users.user_id == tenants.tenant_id)
    if user_tenant is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    db.delete(user_tenant)
    db.commit()
    db.refresh(user_tenant)
    return {'delete tenant successfully with tenant_id': tenant_id}


@router.get('/particular_hostel/{hostel_id}')
def particular_hostel(hostel_id:str, db:db_dependency, current_user:user_dependency, hostel_name:str):
    if detect_attack():
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail='attack detected')
    if current_user is None or current_user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    user = db.query(Users).filter(Users.user_id == current_user.get('user_id')).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    hostel = db.query(HostelRegistration).filter(HostelRegistration.owner_id == user.user_id).filter(HostelRegistration.hostel_name == hostel_name).first()
    if hostel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    tenant = db.query(TenantRegistration).filter(TenantRegistration.hostel_id == hostel_id).first()
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    return tenant

@router.post('/warden')
def warden_access(db:db_dependency, current_user:user_dependency, warden_access: Warden ):
    if current_user is None or current_user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    user = db.query(Users).filter(Users.user_id == current_user.get('user_id')).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='detais not found')
    warden = Users(
        hostel_id = user.hostel_id,
        user_role = 'warden',
        username = warden_access.username,
        password = get_password_hash
    )
    return warden
