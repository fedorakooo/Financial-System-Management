from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Integer, Numeric, DateTime, ForeignKey, Enum, func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base
from src.core.enums.account import AccountStatus


class AccountORM(Base):
    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    enterprise_id: Mapped[int] = mapped_column(Integer, ForeignKey("enterprises.id"), nullable=True)
    bank_id: Mapped[int] = mapped_column(Integer, ForeignKey("banks.id"))
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=2), default=0.0)
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
