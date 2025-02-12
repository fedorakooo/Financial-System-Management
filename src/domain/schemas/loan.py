from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

from src.core.enums.loan import LoanTermMonths, LoanStatus


class LoanBase(BaseModel):
    account_id: int
    amount: int
    term_months: LoanTermMonths
    interest_rate: Decimal
    status: LoanStatus


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    amount: Optional[int] = None
    term_months: Optional[LoanTermMonths] = None
    interest_rate: Optional[Decimal] = None
    status: Optional[LoanStatus] = None


class LoanRead(LoanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
