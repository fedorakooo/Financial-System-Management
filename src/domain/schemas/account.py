from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

from src.core.enums.account import AccountStatus


class AccountBase(BaseModel):
    user_id: int
    enterprise_id: Optional[int] = None
    bank_id: int
    balance: Decimal = Decimal("0.00")
    status: AccountStatus = AccountStatus.ACTIVE


class AccountCreate(AccountBase):
    enterprise_id: Optional[int] = None
    bank_id: int


class AccountUpdate(BaseModel):
    balance: Optional[Decimal] = None
    status: Optional[AccountStatus] = None


class AccountRead(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
