from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.domain.enums.account import AccountStatus


@dataclass(frozen=True)
class Account:
    user_id: int
    bank_id: int
    id: int = None
    balance: Decimal("0.00") = Decimal("0.00")
    status: AccountStatus = AccountStatus.ACTIVE
    created_at: datetime = None
    updated_at: datetime = None
