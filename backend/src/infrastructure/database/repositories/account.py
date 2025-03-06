from typing import List
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.exceptions.repository import NotFoundError
from src.domain.schemas.account import AccountRead, AccountCreate
from src.domain.utils.enums import EnumUtils
from src.infrastructure.database.errors.error_handler import ErrorHandler


class AccountRepository(AbstractAccountRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def get_account_by_id(self, account_id) -> AccountRead:
        stmt = "SELECT * FROM accounts WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchval(stmt, account_id)

        if row:
            return AccountRead(**dict(row))

        raise NotFoundError("Account", "id", account_id)

    async def get_accounts_by_user_id(self, user_id) -> List[AccountRead]:
        stmt = "SELECT * FROM accounts WHERE user_id = $1"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt, user_id)

        return [AccountRead(**dict(row)) for row in rows] if rows else []

    async def create_account(self, account_create: AccountCreate) -> AccountRead:
        account_dict = EnumUtils.convert_enums_to_values(account_create.dict())
        columns = ', '.join(account_dict.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(account_dict))])
        values = tuple(account_dict.values())

        stmt = f"INSERT INTO accounts ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise ErrorHandler.handle_unique_violation("Account", e, account_create)
        except ForeignKeyViolationError as e:
            raise ErrorHandler.handle_unique_violation("Account", e, account_create)

        return AccountRead(**dict(row))

    async def delete_account_by_id(self, account_id: int) -> None:
        stmt = "DELETE FROM accounts WHERE id = $1"

        async with self.db_connection as conn:
            result = await conn.execute(stmt, account_id)

        if result == "DELETE 0":
            raise NotFoundError("Account", "id", account_id)
