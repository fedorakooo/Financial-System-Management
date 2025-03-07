from typing import List
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.exceptions.repository import NotFoundError
from src.domain.schemas.addition import AdditionRead, AdditionCreate
from src.domain.utils.enums import EnumUtils
from src.infrastructure.database.errors.error_handler import ErrorHandler


class AdditionRepository(AbstractAdditionRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def get_addition_by_id(self, addition_id: int) -> AdditionRead:
        stmt = "SELECT * FROM additions WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, addition_id)

        if row:
            return AdditionRead(**dict(row))

        raise NotFoundError("Addition", "id", addition_id)

    async def get_additions(self) -> List[AdditionRead]:
        stmt = "SELECT * FROM additions"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt)

        return [AdditionRead(**dict(row)) for row in rows] if rows else []

    async def get_additions_by_account_id(self, account_id: int) -> List[AdditionRead]:
        stmt = "SELECT * FROM additions WHERE account_id = $1"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt, account_id)

        return [AdditionRead(**dict(row)) for row in rows] if rows else []

    async def create_addition(self, addition_create: AdditionCreate) -> AdditionRead:
        addition_dict = EnumUtils.convert_enums_to_values(addition_create.dict())
        columns = ', '.join(addition_dict.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(addition_dict))])
        values = tuple(addition_dict.values())

        stmt = f"INSERT INTO additions ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("Addition", e, addition_create)
        except ForeignKeyViolationError as e:
            raise ErrorHandler.handle_unique_violation("Addition", e, addition_create)

        return AdditionRead(**dict(row))
