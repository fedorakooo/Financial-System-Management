from datetime import datetime
from sqlalchemy import (
    String, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base


class BankORM(Base):
    __tablename__ = "banks"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    bic: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
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
