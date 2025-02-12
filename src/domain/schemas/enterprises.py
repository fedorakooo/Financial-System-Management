from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.core.enums.enterprise import EnterpriseType


class EnterpriseBase(BaseModel):
    name: str
    type: EnterpriseType
    unp: str
    bank_id: Optional[int]
    address: str


class EnterpriseCreate(EnterpriseBase):
    pass


class EnterpriseUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[EnterpriseType] = None
    unp: Optional[str] = None
    bank_id: Optional[int] = None
    address: Optional[str] = None


class EnterpriseRead(EnterpriseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
