from typing import List
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.entities.addition import Addition
from src.infrastructure.database.handlers.error_handler import ErrorHandler
from src.infrastructure.database.mappers.addition import AdditionDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class AdditionRepository(AbstractAdditionRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def get_addition_by_id(self, addition_id: int) -> Addition:
        stmt = "SELECT * FROM additions WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, addition_id)

        if row:
            return AdditionDatabaseMapper.from_db_row(row)

        raise NotFoundError("Addition with id = {addition_id} not found")

    async def get_additions(self) -> List[Addition]:
        stmt = "SELECT * FROM additions"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt)

        return [AdditionDatabaseMapper.from_db_row(row) for row in rows]

    async def get_additions_by_account_id(self, account_id: int) -> List[Addition]:
        stmt = "SELECT * FROM additions WHERE account_id = $1"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt, account_id)

        return [AdditionDatabaseMapper.from_db_row(row) for row in rows]

    async def create_addition(self, addition_create: Addition) -> Addition:
        addition_create_row = AdditionDatabaseMapper.to_db_row(addition_create)

        columns = ', '.join(addition_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(addition_create_row))])
        values = tuple(addition_create_row.values())

        stmt = f"INSERT INTO additions ({columns}) VALUES ({placeholders}) RETURNING *"
        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Addition", exc, addition_create)
        except ForeignKeyViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Addition", exc, addition_create)

        return AdditionDatabaseMapper.from_db_row(row)
