from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from src.core.enums.user import UserRole


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


class UserUpdate(BaseModel):
    name: Optional[str] = None
    passport_number: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_foreign: Optional[bool] = None
    hashed_password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
