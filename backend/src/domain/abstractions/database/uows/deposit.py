from abc import ABC, abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.deposit import AbstractDepositRepository


class AbstractDepositUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self):
        """Set up the context manager by establishing a connection and starting a transaction."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        """Clean up by committing or rolling back the transaction and closing the connection."""
        pass

    @property
    @abstractmethod
    def deposit_repository(self) -> AbstractDepositRepository:
        """Return the deposit repository."""
        pass

    @property
    @abstractmethod
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass
