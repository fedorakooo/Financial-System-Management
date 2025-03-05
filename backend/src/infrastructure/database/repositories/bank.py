from typing import List
from asyncpg.exceptions import UniqueViolationError

from src.domain.abstractions.repositories.banks import AbstractBankRepository
from src.domain.exceptions.repository import NotFoundError, NoFieldsToUpdateError
from src.domain.schemas.bank import BankRead, BankUpdate, BankCreate
from src.domain.utils.enums import EnumUtils
from src.domain.utils.fields import FieldUtils
from src.infrastructure.database.database import DatabaseConnection
from src.infrastructure.database.errors.error_handler import ErrorHandler


class BankRepository(AbstractBankRepository):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection: DatabaseConnection = db_connection

    async def get_bank_by_id(self, bank_id: int) -> BankRead:
        stmt = "SELECT * FROM banks WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, bank_id)

        if row is None:
            raise NotFoundError("Bank", "id", bank_id)

        return BankRead(**dict(row))

    async def get_banks(self) -> List[BankRead]:
        stmt = "SELECT * FROM banks"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt)

        return [BankRead(**dict(row)) for row in rows] if rows else []

    async def create_bank(self, bank_create: BankCreate) -> BankRead:
        bank_dict = EnumUtils.convert_enums_to_values(bank_create.dict())
        columns = ', '.join(bank_dict.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(bank_dict))])
        values = tuple(bank_dict.values())

        stmt = f"INSERT INTO banks ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("Bank", e, bank_create)

        return BankRead(**dict(row))

    async def update_bank_by_id(self, bank_id: int, bank_update: BankUpdate) -> BankRead:
        updated_fields = FieldUtils.get_updated_fields(dict(bank_update))

        if not updated_fields:
            raise NoFieldsToUpdateError()

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(updated_fields.keys())])
        values = tuple(updated_fields.values()) + (bank_id,)
        stmt = f"UPDATE banks SET {columns} WHERE id = ${len(values)} RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("Bank", e, bank_update)

        if row:
            return BankRead(**dict(row))

        raise NotFoundError("Bank", "id", bank_id)

    async def delete_bank_by_id(self, bank_id: int) -> None:
        stmt = "DELETE FROM banks WHERE id = $1"

        async with self.db_connection as conn:
            result = await conn.execute(stmt, bank_id)

        if result == "DELETE 0":
            raise NotFoundError("Bank", "id", bank_id)
