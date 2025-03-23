from abc import ABC, abstractmethod

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.factories.repository import AbstractRepositoryFactory
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.transfer import AbstractTransferRepository


class AbstractTransferUnitOfWork(ABC):
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
    def account_repository(self) -> AbstractAccountRepository:
        """Return the account repository."""
        pass

    @property
    @abstractmethod
    def transfer_repository(self) -> AbstractTransferRepository:
        """Return the transfer repository."""
        pass