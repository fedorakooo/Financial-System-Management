from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.installment import InstallmentTermMonths, InstallmentStatus
from src.domain.utils.partial_model import partial_model


class InstallmentBase(BaseModel):
    account_id: int
    amount: int
    term_months: InstallmentTermMonths
    interest_rate: Decimal
    status: InstallmentStatus


class InstallmentCreate(InstallmentBase):
    pass


@partial_model
class InstallmentUpdate(InstallmentBase):
    pass


class InstallmentRead(InstallmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
