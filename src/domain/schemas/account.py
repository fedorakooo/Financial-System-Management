from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

from src.domain.enums.account import AccountStatus
from src.domain.utils.partial_model import partial_model


class AccountBase(BaseModel):
    user_id: int
    enterprise_id: Optional[int] = None
    bank_id: int
    balance: Decimal = Decimal("0.00")
    status: AccountStatus = AccountStatus.ACTIVE


class AccountCreate(AccountBase):
    enterprise_id: Optional[int] = None
    bank_id: int


@partial_model
class AccountUpdate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
