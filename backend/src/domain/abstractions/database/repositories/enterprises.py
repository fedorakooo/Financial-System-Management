from abc import ABC, abstractmethod
from typing import List

from src.domain.schemas.enterprise import EnterpriseRead, EnterpriseCreate, EnterpriseUpdate


class AbstractEnterpriseRepository(ABC):
    """Abstract class for an enterprise repository."""

    @abstractmethod
    async def get_enterprise_by_id(self, enterprise_id) -> EnterpriseRead:
        """Fetches an enterprise by its unique identifier.

        Raises:
            NotFoundError: If the enterprise with the specified id is not found.
        """
        pass

    @abstractmethod
    async def get_enterprises(self) -> List[EnterpriseRead]:
        """Fetches all enterprises from the repository."""
        pass

    @abstractmethod
    async def create_enterprise(self, enterprise_create: EnterpriseCreate) -> EnterpriseRead:
        """Creates a new enterprise.

        Raises:
            UniqueConstraintError: If there is a violation of unique constraints.
        """
        pass

    @abstractmethod
    async def update_enterprise_by_id(self, enterprise_id: int, enterprise_update: EnterpriseUpdate) -> EnterpriseRead:
        """Updates an enterprise by its unique identifier.

        Raises:
            NotFoundError: If the enterprise with the specified id is not found.
            NoFieldsToUpdateError: If no fields are provided for updating.
            UniqueConstraintError: If there is a violation of unique constraints.
        """
        pass

    @abstractmethod
    async def delete_enterprise_by_id(self, enterprise_id: int) -> None:
        """Deletes an enterprise by its unique identifier.

        Raises:
            NotFoundError: If the enterprise with the specified id is not found.
        """
        pass
