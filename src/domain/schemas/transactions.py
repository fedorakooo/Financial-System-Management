from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from src.core.enums.transaction import TransactionType, TransactionStatus


class TransactionBase(BaseModel):
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    amount: int
    type: TransactionType
    status: TransactionStatus


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    amount: Optional[int] = None
    type: Optional[TransactionType] = None
    status: Optional[TransactionStatus] = None


class TransactionRead(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
