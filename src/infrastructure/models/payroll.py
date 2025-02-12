from datetime import datetime
from sqlalchemy import Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base
from src.core.enums.payroll import PayrollRequestStatus


class PayrollRequestORM(Base):
    __tablename__ = "payroll_requests"

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"))
    status: Mapped[PayrollRequestStatus] = mapped_column(Enum(PayrollRequestStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
