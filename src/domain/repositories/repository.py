from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, item) -> None:
        """Adds one item to the repository."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> List:
        """Returns all items from the repository."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: int) -> Optional:
        """Finds an item by its id, or returns None if not found."""
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, item) -> None:
        """Updates one item in the repository by its id."""
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> None:
        """Deletes one item from the repository by its id."""
        raise NotImplementedError
