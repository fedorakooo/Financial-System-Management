from sqlalchemy import (
    select, insert, update, delete
)
from typing import Optional, List, TypeVar, Generic
from pydantic import BaseModel

from src.domain.repositories.repository import AbstractRepository
from src.infrastructure.uow import UnitOfWork

Item = TypeVar("Item", bound=BaseModel)


class SQLAlchemyRepository(Generic[Item], AbstractRepository):
    model = None

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_one(self, item: Item) -> Item:
        query = insert(self.model).values(**item.__dict__).returning(self.model.id)
        result = await self.uow.session.execute(query)
        item_id = result.scalar_one()
        return await self.find_by_id(item_id)

    async def find_all(self) -> List[Item]:
        query = select(self.model)
        result = await self.uow.session.execute(query)
        return result.scalars().all()

    async def find_by_id(self, id: int) -> Item:
        query = select(self.model).where(self.model.id == id)
        result = await self.uow.session.execute(query)
        item = result.scalar_one_or_none()
        if item is None:
            raise ValueError(f"Item with id {id} not found.")
        return Item

    async def update_one(self, id: int, item: Item) -> Optional[Item]:
        query = update(self.model).where(self.model.id == id).values(**item.__dict__)
        result = await self.uow.session.execute(query)
        if result.rowcount == 0:
            raise ValueError(f"Item with id {id} not found.")
        return await self.find_by_id(id)

    async def delete_one(self, id: int) -> None:
        query = delete(self.model).where(self.model.id == id)
        result = await self.uow.session.execute(query)
        if result.rowcount == 0:
            raise ValueError(f"Item with id {id} not found.")
