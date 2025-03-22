from decimal import Decimal
from asyncpg import UniqueViolationError, ForeignKeyViolationError

from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.transfer_manager import AbstractTransferManagerRepository
from src.domain.entities.transfer import Transfer
from src.infrastructure.database.handlers.error_handler import ErrorHandler
from src.infrastructure.database.mappers.transfer import TransferDatabaseMapper


class TransferManagerRepository(AbstractTransferManagerRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def create_transfer_with_balance_updates(
            self,
            transfer_create: Transfer,
            new_sender_balance: Decimal,
            new_receiver_balance: Decimal
    ) -> Transfer:
        transfer_create_row = TransferDatabaseMapper.to_db_row(transfer_create)

        columns = ', '.join(transfer_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(transfer_create_row))])
        values = tuple(transfer_create_row.values())

        stmt_insert_transfer = f"INSERT INTO transfers ({columns}) VALUES ({placeholders}) RETURNING *"

        stmt_update_sender_account = "UPDATE accounts SET balance = $2 WHERE id = $1"
        stmt_update_receiver_account = "UPDATE accounts SET balance = $2 WHERE id = $1"

        try:
            async with self.db_connection as conn:
                row = await conn.fetchrow(stmt_insert_transfer, *values)
                await conn.execute(stmt_update_sender_account, transfer_create.from_account_id, new_sender_balance)
                await conn.execute(stmt_update_receiver_account, transfer_create.to_account_id, new_receiver_balance)
        except UniqueViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Transfer", exc, transfer_create)
        except ForeignKeyViolationError as exc:
            raise ErrorHandler.handle_unique_violation("Transfer", exc, transfer_create)

        return TransferDatabaseMapper.from_db_row(row)
