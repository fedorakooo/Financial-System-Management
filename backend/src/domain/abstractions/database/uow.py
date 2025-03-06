from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    """Abstract class for unit of work pattern."""

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUnitOfWork':
        """Asynchronous method for entering the context (starting the transaction)."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Asynchronous method for exiting the context (completing the transaction)."""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """Method to commit (save changes) to the database."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Method to rollback (discard changes) in the database."""
        pass

    @classmethod
    @abstractmethod
    def get_unit_of_work(cls) -> 'AbstractUnitOfWork':
        """Factory method for creating and returning a new UnitOfWork instance."""
        pass
