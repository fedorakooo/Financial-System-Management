from abc import ABC, abstractmethod
from typing import List

from src.domain.schemas.bank import BankRead, BankUpdate, BankCreate


class AbstractBankRepository(ABC):
    """Abstract class for a bank repository."""

    @abstractmethod
    async def get_bank_by_id(self, bank_id: int) -> BankRead:
        """Fetches a bank by its unique identifier.

        Raises:
            NotFoundError: If the bank with the specified id is not found.
        """
        pass

    @abstractmethod
    async def get_banks(self) -> List[BankRead]:
        """Fetches all banks from the repository."""
        pass

    @abstractmethod
    async def create_bank(self, bank_create: BankCreate) -> BankRead:
        """Creates a new bank.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass

    @abstractmethod
    async def update_bank_by_id(self, bank_id: int, bank_update: BankUpdate) -> BankRead:
        """Updates a bank by its unique identifier.

        Raises:
            NotFoundError: If the bank with the specified id is not found.
            NoFieldsToUpdateError: If no fields are provided for updating.
            UniqueConstraintError: If there is a violation of unique constraints.
        """
        pass

    @abstractmethod
    async def delete_bank_by_id(self, bank_id: int) -> None:
        """Deletes a bank by its unique identifier.

        Raises:
            NotFoundError: If the bank with the specified id is not found.
        """
        pass
