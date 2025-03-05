from datetime import datetime
from pydantic import BaseModel, EmailStr

from src.domain.enums.user import UserRole
from src.domain.utils.models import ModelUtils


class UserBase(BaseModel):
    name: str
    passport_number: str
    phone_number: str
    email: EmailStr
    role: UserRole
    is_active: bool = False
    is_foreign: bool


class UserCreate(UserBase):
    hashed_password: str


@ModelUtils.partial_model
class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
