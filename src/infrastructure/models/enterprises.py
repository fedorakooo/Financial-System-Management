from datetime import datetime
from sqlalchemy import (
    String, Integer, DateTime, Enum, ForeignKey, func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base
from src.core.enums.enterprise import EnterpriseType


class EnterpriseORM(Base):
    __tablename__ = "enterprises"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    type: Mapped[EnterpriseType] = mapped_column(Enum(EnterpriseType), nullable=False)
    unp: Mapped[str] = mapped_column(String(32), nullable=False)
    bank_id: Mapped[int] = mapped_column(Integer, ForeignKey("banks.id"))
    address: Mapped[str] = mapped_column(String(255), nullable=False)
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
