from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

from src.domain.enums.account import AccountStatus
from src.domain.utils.model import ModelUtils


class AccountBase(BaseModel):
    enterprise_id: Optional[int] = None
    bank_id: int
    balance: Decimal = Decimal("0.00")
    status: AccountStatus = AccountStatus.ACTIVE


class AccountCreate(AccountBase):
    user_id: int


class AccountCreateRequest(AccountBase):
    pass


@ModelUtils.partial_model
class AccountUpdate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
