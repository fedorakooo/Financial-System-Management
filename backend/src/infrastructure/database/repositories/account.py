from decimal import Decimal
from typing import List
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.entities.account import Account
from src.infrastructure.database.handlers.error_handler import ErrorHandler
from src.infrastructure.database.mappers.account import AccountDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class AccountRepository(AbstractAccountRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def get_account_by_id(self, account_id) -> Account:
        stmt = "SELECT * FROM accounts WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, account_id)

        if row:
            return AccountDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"Account with id {account_id} not found")

    async def get_accounts_by_user_id(self, user_id) -> List[Account]:
        stmt = "SELECT * FROM accounts WHERE user_id = $1"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt, user_id)

        return [AccountDatabaseMapper.from_db_row(row) for row in rows] if rows else []

    async def create_account(self, account_create: Account) -> Account:
        account_create_row = AccountDatabaseMapper.to_db_row(account_create)

        columns = ', '.join(account_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(account_create_row))])
        values = tuple(account_create_row.values())

        stmt = f"INSERT INTO accounts ({columns}) VALUES ({placeholders}) RETURNING *"

        try:
            async with self.db_connection as conn:
                print(values)
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Account", exc, account_create)
        except ForeignKeyViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Account", exc, account_create)

        return AccountDatabaseMapper.from_db_row(row)

    async def update_account(self, account_id: int, account_update: Account) -> Account:
        account_update_row = AccountDatabaseMapper.to_db_row(account_update)

        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(account_update_row.keys())])
        values = tuple(account_update_row.values()) + (account_id,)
        print(account_update_row)
        stmt = f"UPDATE accounts SET {columns} WHERE id = ${len(values)} RETURNING *"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt, *values)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Account", exc, account_update)

        if row:
            return AccountDatabaseMapper.from_db_row(row)

        raise NotFoundError(f"Account with id {account_id} not found")


    async def update_account_balance(self, account_id: int, amount: Decimal) -> Account:
        account: Account = await self.get_account_by_id(account_id)

        new_balance = account.balance + amount

        stmt = "UPDATE accounts SET balance = $2 WHERE id = $1 RETURNING *"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, account_id, new_balance)

        return AccountDatabaseMapper.from_db_row(row)

    async def delete_account_by_id(self, account_id: int) -> None:
        stmt = "DELETE FROM accounts WHERE id = $1"

        async with self.db_connection as conn:
            result = await conn.execute(stmt, account_id)

        if result == "DELETE 0":
            raise NotFoundError(f"Account with id {account_id} not found")
