from datetime import datetime
from pydantic import BaseModel

from src.domain.enums.payroll import PayrollRequestStatus
from src.domain.utils.partial_model import partial_model


class PayrollRequestBase(BaseModel):
    enterprise_id: int
    status: PayrollRequestStatus


class PayrollRequestCreate(PayrollRequestBase):
    pass


@partial_model
class PayrollRequestUpdate(PayrollRequestBase):
    pass


class PayrollRequestRead(PayrollRequestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
