from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Integer, DateTime, Numeric, ForeignKey, Enum, func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base
from src.core.enums.installment import InstallmentStatus, InstallmentTermMonths


class InstallmentORM(Base):
    __tablename__ = "installments"

    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    term_months: Mapped[InstallmentTermMonths] = mapped_column(Enum(InstallmentTermMonths), nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(precision=6, scale=2), nullable=False)
    status: Mapped[InstallmentStatus] = mapped_column(Enum(InstallmentStatus), nullable=False)
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
