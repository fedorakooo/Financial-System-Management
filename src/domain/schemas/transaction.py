from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from src.domain.enums.transaction import TransactionType, TransactionStatus
from src.domain.utils.partial_model import partial_model


class TransactionBase(BaseModel):
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    amount: int
    type: TransactionType
    status: TransactionStatus


class TransactionCreate(TransactionBase):
    pass


@partial_model
class TransactionUpdate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
