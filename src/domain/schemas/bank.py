from datetime import datetime
from pydantic import BaseModel

from src.domain.utils.partial_model import partial_model


class BankBase(BaseModel):
    name: str
    bic: str
    address: str


class BankCreate(BankBase):
    pass


@partial_model
class BankUpdate(BankBase):
    pass


class BankRead(BankBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
