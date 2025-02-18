from abc import abstractmethod, ABC
from typing import Optional, List, TypeVar, Generic, Type
from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel

from src.domain.abstractions.repository import AbstractRepository
from src.infrastructure.database import DatabaseConnection
from src.domain.exceptions.repository import (
    UniqueConstraintError,
    NoFieldsToUpdateError,
    NotFoundError
)

Item = TypeVar("Item", bound=BaseModel)


class SQLRepository(Generic[Item], AbstractRepository, ABC):
    """Abstract base class for SQL repositories that must be inherited."""

    table_name: str = None
    model_class: Type[Item]

    def __init__(self):
        self.db_connection = DatabaseConnection()

    @classmethod
    @abstractmethod
    def create_table(cls) -> None:
        pass

    async def find_by_id(self, id: int) -> Optional[Item]:
        stmt = f"SELECT * FROM {self.table_name} WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, id)

        if row is None:
            return None

        return self.model_class(**dict(row))

    async def find_all(self) -> List[Item]:
        stmt = f"SELECT * FROM {self.table_name}"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt)

        return [self.model_class(**dict(row)) for row in rows]

    async def add_one(self, item: Item) -> Item:
        columns = ', '.join(item.dict().keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(item.dict()))])
        values = item.dict().values()
        stmt = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING id"

        try:
            async with self.db_connection as conn:
                item_id = await conn.fetchval(stmt, *values)
        except UniqueViolationError:
            bic_value = item.dict().get('bic', 'Unknown')
            raise UniqueConstraintError('bic', bic_value)

        return await self.find_by_id(item_id)

    async def update_one(self, id: int, item: Item) -> Optional[Item]:
        updated_fields = {key: value for key, value in item.dict().items() if value is not None}

        if not updated_fields:
            raise NoFieldsToUpdateError()

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(updated_fields.keys())])
        values = tuple(updated_fields.values()) + (id,)
        stmt = f"UPDATE {self.table_name} SET {columns} WHERE id = ${len(values)}"

        try:
            async with self.db_connection as conn:
                result = await conn.execute(stmt, *values)
        except UniqueViolationError:
            bic_value = item.dict().get('bic', 'Unknown')
            raise UniqueConstraintError('bic', bic_value)

        if result == "UPDATE 0":
            raise NotFoundError(id)

        return await self.find_by_id(id)

    async def delete_one(self, id: int) -> None:
        stmt = f"DELETE FROM {self.table_name} WHERE id = $1"

        async with self.db_connection as conn:
            result = await conn.execute(stmt, id)

        if result == "DELETE 0":
            raise NotFoundError(id)
