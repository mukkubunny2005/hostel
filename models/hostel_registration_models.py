from pydantic import BaseModel, Field
from typing import Optional
from models.hostel_registration_models import GenderEnum


class HostelRequest(BaseModel):
    hostel_name: str = Field(...)
    area: str = Field(...)
    city: str = Field(...)
    state: str = Field(...)
    gender: GenderEnum = Field(...)
    phone_number: str = Field(..., min_length=7, max_length=15)

    veg: bool = Field(..., default=False)
    non_veg: bool = Field(..., default=False)
    ac: bool = Field(..., default=False)
    non_ac: bool = Field(..., default=False)

    no_of_ac_beds: int = Field(..., default=0)
    no_of_non_ac_beds: int = Field(..., default=0)

    non_ac_sharing: bool = Field(..., default=False)
    non_ac_sharing_price: float = Field(..., default=8000.00)
    ac_sharing: bool = Field(..., default=False)
    ac_sharing_price: float = Field(..., default=5000.00)

    monday: str = Field(...,)
    tuesday: str = Field(...)
    wednesday: str = Field(...)
    thursday: str = Field(...)
    friday: str = Field(...)
    saturday: str = Field(...)
    sunday: str = Field(...)

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

    wifi_screens: str = Field(...)
    wifi_password: str = Field(...)

    terms_and_conditions: str = Field(...)
    rules_and_regulations: str = Field(...)

    class Config:
        anystr_strip_whitespace = True
        extra = "forbid"
        orm_mode = True
        