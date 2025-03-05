from abc import ABC, abstractmethod
from typing import List

from src.domain.schemas.account import AccountRead, AccountCreate


class AbstractAccountRepository(ABC):
    """Abstract class for an account repository."""

    @abstractmethod
    async def get_account_by_id(self, account_id) -> AccountRead:
        """Fetches an account by its unique identifier.

        Raises:
            NotFoundError: If the account with the specified id is not found.
        """
        pass

    @abstractmethod
    async def get_accounts_by_user_id(self, user_id) -> List[AccountRead]:
        """Fetches all accounts associated with a specific user."""
        pass

    @abstractmethod
    async def create_account(self, account_create: AccountCreate) -> AccountRead:
        """Creates a new account.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass

    @abstractmethod
    async def delete_account_by_id(self, account_id: int) -> None:
        """Deletes an account by its unique identifier.

        Raises:
            NotFoundError: If the account with the specified id is not found.
        """
        pass
