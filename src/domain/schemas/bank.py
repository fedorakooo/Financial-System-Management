from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BankBase(BaseModel):
    name: str
    bic: str
    address: str


class BankCreate(BankBase):
    pass


class BankUpdate(BaseModel):
    name: Optional[str] = None
    bic: Optional[str] = None
    address: Optional[str] = None


class BankRead(BankBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
