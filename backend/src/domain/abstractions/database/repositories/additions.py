from abc import ABC, abstractmethod
from typing import List

from src.domain.schemas.addition import AdditionRead, AdditionCreate


class AbstractAdditionRepository(ABC):
    """Abstract class for an addition repository."""

    @abstractmethod
    async def get_addition_by_id(self, addition_id: int) -> AdditionRead:
        """Fetches an addition by its unique identifier.

        Raises:
            NotFoundError: If the addition with the specified id is not found."""
        pass

    @abstractmethod
    async def get_additions(self) -> List[AdditionRead]:
        """Fetches all additions from the repository."""
        pass

    @abstractmethod
    async def get_additions_by_account_id(self, account_id: int) -> List[AdditionRead]:
        """Fetches all additions associated with a specific user."""
        pass

    async def create_addition(self, addition_create: AdditionCreate) -> AdditionRead:
        """Creates a new addition.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
            ForeignKeyError: If a foreign key constraint violation occurs.
        """
        pass
