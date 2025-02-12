from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Integer, DateTime, ForeignKey, Numeric, Enum, func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base
from src.core.enums.loan import LoanStatus, LoanTermMonths


class LoanORM(Base):
    __tablename__ = "loans"

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    term_months: Mapped[LoanTermMonths] = mapped_column(Enum(LoanTermMonths), nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(precision=6, scale=2), nullable=False)
    status: Mapped[LoanStatus] = mapped_column(Enum(LoanStatus), nullable=False)
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
