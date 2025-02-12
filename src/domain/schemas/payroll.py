from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.core.enums.payroll import PayrollRequestStatus


class PayrollRequestBase(BaseModel):
    enterprise_id: int
    status: PayrollRequestStatus


class PayrollRequestCreate(PayrollRequestBase):
    pass


class PayrollRequestUpdate(BaseModel):
    status: Optional[PayrollRequestStatus] = None


class PayrollRequestRead(PayrollRequestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
