from abc import ABC, abstractmethod

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository


class AbstractAdditionUnitOfWork(ABC):
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
    def addition_repository(self) -> AbstractAdditionRepository:
        """Return the addition repository."""
        pass
