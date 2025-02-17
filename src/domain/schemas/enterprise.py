from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.domain.enums.enterprise import EnterpriseType
from src.domain.utils.partial_model import partial_model


class EnterpriseBase(BaseModel):
    name: str
    type: EnterpriseType
    unp: str
    bank_id: Optional[int]
    address: str


class EnterpriseCreate(EnterpriseBase):
    pass


@partial_model
class EnterpriseUpdate(EnterpriseBase):
    pass


class EnterpriseRead(EnterpriseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
