from typing import List
from asyncpg.exceptions import UniqueViolationError

from src.domain.abstractions.database.repositories.enterprises import AbstractEnterpriseRepository
from src.domain.exceptions.repository import NotFoundError, NoFieldsToUpdateError
from src.domain.schemas.enterprise import EnterpriseRead, EnterpriseCreate, EnterpriseUpdate
from src.domain.utils.enums import EnumUtils
from src.domain.utils.fields import FieldUtils
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.errors.error_handler import ErrorHandler


class EnterpriseRepository(AbstractEnterpriseRepository):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection: DatabaseConnection = db_connection

    async def get_enterprise_by_id(self, enterprise_id) -> EnterpriseRead:
        stmt = "SELECT * FROM enterprises where id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, enterprise_id)

        return EnterpriseRead(**dict(row))

    async def get_enterprises(self) -> List[EnterpriseRead]:
        stmt = "SELECT * FROM enterprises"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt)

        return [EnterpriseRead(**dict(row)) for row in rows]

    async def create_enterprise(self, enterprise_create: EnterpriseCreate) -> EnterpriseRead:
        enterprise_dict = EnumUtils.convert_enums_to_values(dict(enterprise_create))
        columns = ', '.join(enterprise_dict.keys())
        placeholders = [f"${i + 1}" for i in range(len(enterprise_dict))]
        values = ', '.join(enterprise_dict.values())

        stmt = f"INSERT INTO enterprises ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("Enterprise", e, enterprise_create)

        return EnterpriseRead(**dict(row))

    async def update_enterprise_by_id(self, enterprise_id: int, enterprise_update: EnterpriseUpdate) -> EnterpriseRead:
        updated_fields = FieldUtils.get_updated_fields(dict(enterprise_update))

        if not updated_fields:
            raise NoFieldsToUpdateError()

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(updated_fields.keys())])
        values = tuple(updated_fields.values()) + (enterprise_id,)
        stmt = f"UPDATE banks SET {columns} WHERE id = ${len(values)} RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("Enterprise", e, enterprise_update)

        if row:
            return EnterpriseRead(**dict(row))

        raise NotFoundError("Bank", "id", enterprise_id)

    async def delete_enterprise_by_id(self, enterprise_id: int) -> None:
        stmt = "DELETE FROM enterprises WHERE id = $1"

        async with self.db_connection as conn:
            result = await conn.execute(stmt, enterprise_id)

        if result == "DELETE 0":
            raise NotFoundError("Enterprise", "id", enterprise_id)
