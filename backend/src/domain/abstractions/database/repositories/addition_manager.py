from abc import ABC, abstractmethod
from decimal import Decimal

from src.domain.entities.addition import Addition


class AbstractAdditionManagerRepository(ABC):
    @abstractmethod
    async def create_addition_with_balance_updates(
            self,
            addition_create: Addition,
            new_account_balance: Decimal
    ) -> Addition:
        """Creates a new addition record and updates the account balance in a single transaction.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass
