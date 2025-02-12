from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

from src.core.enums.installment import InstallmentTermMonths, InstallmentStatus


class InstallmentBase(BaseModel):
    account_id: int
    amount: int
    term_months: InstallmentTermMonths
    interest_rate: Decimal
    status: InstallmentStatus


class InstallmentCreate(InstallmentBase):
    pass


class InstallmentUpdate(BaseModel):
    status: Optional[InstallmentStatus] = None


class InstallmentRead(InstallmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
