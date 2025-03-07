from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from src.domain.enums.addition import AdditionSource, AdditionStatus


class AdditionBase(BaseModel):
    amount: Decimal = Decimal("0.00")
    account_id: int
    source: AdditionSource
    status: AdditionStatus = AdditionStatus.PENDING


class AdditionCreate(AdditionBase):
    account_id: int


class AdditionRead(AdditionBase):
    id: int
    created_at: datetime
