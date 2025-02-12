from datetime import datetime
from sqlalchemy import Integer, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.infrastructure.database import Base
from src.core.enums.transaction import TransactionType, TransactionStatus


class TransactionORM(Base):
    __tablename__ = "transactions"

    from_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    to_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    @validates('from_account_id', 'to_account_id')
    def validate_accounts(self, key, value):
        if (key == 'from_account_id' and value is None and self.to_account_id is None) or \
                (key == 'to_account_id' and value is None and self.from_account_id is None):
            raise ValueError("At least one of from_account_id or to_account_id must have a value")
        return value
