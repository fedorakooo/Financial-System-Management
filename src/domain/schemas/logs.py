from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class LogBase(BaseModel):
    user_id: int
    action: str
    details: Optional[str] = None


class LogRead(LogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
