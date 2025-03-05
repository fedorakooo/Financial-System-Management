from datetime import datetime
from pydantic import BaseModel

from src.domain.utils.model import ModelUtils


class BankBase(BaseModel):
    name: str
    bic: str
    address: str


class BankCreate(BankBase):
    pass


@ModelUtils.partial_model
class BankUpdate(BankBase):
    pass


class BankRead(BankBase):
    id: int
    created_at: datetime
    updated_at: datetime
