from abc import ABC, abstractmethod

from src.domain.abstractions.database.repositories.banks import AbstractBankRepository


class AbstractBankUnitOfWork(ABC):

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
    def bank_repository(self) -> AbstractBankRepository:
        """Return the account repository."""
        pass
