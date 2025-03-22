from abc import ABC, abstractmethod
from decimal import Decimal

from src.domain.entities.withdrawal import Withdrawal


class AbstractWithdrawalManagerRepository(ABC):
    @abstractmethod
    async def create_withdrawal_with_balance_updates(
            self,
            withdrawal_create: Withdrawal,
            new_account_balance: Decimal
    ) -> Withdrawal:
        """Creates a new withdrawal record and updates the account balance in a single transaction.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
            InsufficientFundsError: If the new balance would result in a negative value (if applicable).
        """
        pass
