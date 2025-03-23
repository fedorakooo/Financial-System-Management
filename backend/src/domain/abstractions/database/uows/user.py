from abc import ABC, abstractmethod

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.factories.repository import AbstractRepositoryFactory
from src.domain.abstractions.database.repositories.users import AbstractUserRepository


class AbstractUserUnitOfWork(ABC):
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
    def user_repository(self) -> AbstractUserRepository:
        """Return the user repository."""
        pass
