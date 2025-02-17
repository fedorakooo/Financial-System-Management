from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.loan import LoanTermMonths, LoanStatus
from src.domain.utils.partial_model import partial_model


class LoanBase(BaseModel):
    account_id: int
    amount: int
    term_months: LoanTermMonths
    interest_rate: Decimal
    status: LoanStatus


class LoanCreate(LoanBase):
    pass


@partial_model
class LoanUpdate(LoanBase):
    pass


class LoanRead(LoanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
