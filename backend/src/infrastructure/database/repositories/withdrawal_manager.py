from decimal import Decimal
from asyncpg import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.withdrawal_manager import AbstractWithdrawalManagerRepository
from src.domain.entities.withdrawal import Withdrawal
from src.infrastructure.database.handlers.error_handler import ErrorHandler
from src.infrastructure.database.mappers.withdrawal import WithdrawalDatabaseMapper


class WithdrawalManagerRepository(AbstractWithdrawalManagerRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def create_withdrawal_with_balance_updates(
            self,
            withdrawal_create: Withdrawal,
            new_account_balance: Decimal
    ) -> Withdrawal:
        withdrawal_create_row = WithdrawalDatabaseMapper.to_db_row(withdrawal_create)

        columns = ', '.join(withdrawal_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(withdrawal_create_row))])
        values = tuple(withdrawal_create_row.values())

        stmt_insert_withdrawal = f"INSERT INTO withdrawals ({columns}) VALUES ({placeholders}) RETURNING *"

        stmt_update_account = "UPDATE accounts SET balance = $2 WHERE id = $1"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt_insert_withdrawal, *values)
                await conn.execute(stmt_update_account, withdrawal_create.account_id, new_account_balance)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Withdrawal", exc, withdrawal_create)
        except ForeignKeyViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Withdrawal", exc, withdrawal_create)

        return WithdrawalDatabaseMapper.from_db_row(row)
