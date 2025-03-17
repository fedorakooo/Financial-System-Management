from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.domain.enums.addition import AdditionSource, AdditionStatus


@dataclass(frozen=True)
class Addition:
    account_id: int
    amount: Decimal("0.00")
    source: AdditionSource
    id: Optional[int] = None
    status: AdditionStatus = AdditionStatus.COMPLETED
    created_at: Optional[datetime] = None
