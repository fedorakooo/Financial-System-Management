from typing import List
from asyncpg.exceptions import UniqueViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.exceptions.repository import NoFieldsToUpdateError, NotFoundError
from src.domain.schemas.user import UserRead, UserCreate, UserUpdate
from src.domain.utils.enums import EnumUtils
from src.domain.utils.fields import FieldUtils
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.errors.error_handler import ErrorHandler


class UserRepository(AbstractUserRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def get_user_by_id(self, user_id: int) -> UserRead:
        stmt = "SELECT * FROM users WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, user_id)

        if row:
            return UserRead(**dict(row))

        raise NotFoundError('User', 'id', user_id)

    async def get_user_by_phone_number(self, phone_number: str) -> UserRead:
        stmt = "SELECT * FROM users WHERE phone_number = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, phone_number)
        if row:
            return UserRead(**dict(row))

        raise NotFoundError('User', 'phone_number', phone_number)

    async def get_user_hashed_password_by_phone_number(self, phone_number: str) -> str:
        stmt = "SELECT hashed_password FROM users WHERE phone_number = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, phone_number)

        if row:
            return row['hashed_password']

        raise NotFoundError('User', 'phone_number', phone_number)

    async def get_users(self) -> List[UserRead]:
        stmt = "SELECT * FROM users"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt)

        return [UserRead(**dict(row)) for row in rows] if rows else []

    async def create_user(self, user_create: UserCreate) -> UserRead:
        bank_dict = EnumUtils.convert_enums_to_values(user_create.dict())
        columns = ', '.join(bank_dict.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(bank_dict))])
        values = tuple(bank_dict.values())

        stmt = f"INSERT INTO users ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("User", e, user_create)

        return UserRead(**dict(row))

    async def update_user_by_id(self, user_id: int, user_update: UserUpdate) -> UserRead:
        updated_fields = FieldUtils.get_updated_fields(dict(user_update))

        if not updated_fields:
            raise NoFieldsToUpdateError()

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(updated_fields.keys())])
        values = tuple(updated_fields.values()) + (user_id,)
        stmt = f"UPDATE users SET {columns} WHERE id = ${len(values)} RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("User", e, user_update)

        if row:
            return UserRead(**dict(row))

        raise NotFoundError("User", "id", user_id)

    async def delete_user_by_id(self, user_id: int) -> None:
        stmt = "DELETE FROM users WHERE id = $1"

        async with self.db_connection as conn:
            result = await conn.execute(stmt, user_id)

        if result == "DELETE 0":
            raise NotFoundError("User", "id", user_id)
