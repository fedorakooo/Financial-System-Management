from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar
from pydantic import BaseModel

Item = TypeVar('Item', bound=BaseModel)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, item: Item) -> Item:
        """Adds one item to the repository."""
        pass

    @abstractmethod
    async def find_all(self) -> List[Item]:
        """Returns all items from the repository."""
        pass

    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[Item]:
        """Finds an item by its id, or returns None if not found."""
        pass

    @abstractmethod
    async def update_one(self, id: int, item: Item) -> Item:
        """Updates one item in the repository by its id."""
        pass

    @abstractmethod
    async def delete_one(self, id: int) -> None:
        """Deletes one item from the repository by its id."""
        pass
