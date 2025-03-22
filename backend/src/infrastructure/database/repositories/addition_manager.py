from decimal import Decimal
from asyncpg import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.addition_manager import AbstractAdditionManagerRepository
from src.domain.entities.addition import Addition
from src.infrastructure.database.handlers.error_handler import ErrorHandler
from src.infrastructure.database.mappers.addition import AdditionDatabaseMapper


class AdditionManagerRepository(AbstractAdditionManagerRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def create_addition_with_balance_updates(
            self,
            addition_create: Addition,
            new_account_balance: Decimal
    ) -> Addition:
        addition_create_row = AdditionDatabaseMapper.to_db_row(addition_create)

        columns = ', '.join(addition_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(addition_create_row))])
        values = tuple(addition_create_row.values())

        stmt_insert_addition = f"INSERT INTO additions ({columns}) VALUES ({placeholders}) RETURNING *"

        stmt_update_account = "UPDATE accounts SET balance = $2 WHERE id = $1"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt_insert_addition, *values)
                await conn.execute(stmt_update_account, addition_create.account_id, new_account_balance)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Addition", exc, addition_create)
        except ForeignKeyViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Addition", exc, addition_create)

        return AdditionDatabaseMapper.from_db_row(row)
