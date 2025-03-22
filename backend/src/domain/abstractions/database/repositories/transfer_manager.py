from abc import ABC, abstractmethod
from decimal import Decimal

from src.domain.entities.transfer import Transfer


class AbstractTransferManagerRepository(ABC):
    @abstractmethod
    async def create_transfer_with_balance_updates(
            self,
            transfer_create: Transfer,
            new_sender_balance: Decimal,
            new_receiver_balance: Decimal
    ) -> Transfer:
        """Creates a new transfer record and updates the balances of both sender and receiver accounts in a single transaction.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass
