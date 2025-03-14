from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    """Abstract class for unit of work pattern."""

    @abstractmethod
    async def commit(self) -> None:
        """Method to commit (save changes) to the database."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Method to rollback (discard changes) in the database."""
        pass
