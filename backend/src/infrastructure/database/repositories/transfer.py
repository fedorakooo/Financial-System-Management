from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.transfer import AbstractTransferRepository
from src.domain.entities.transfer import Transfer
from src.infrastructure.database.mappers.transfer import TransferDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class TransferRepository(AbstractTransferRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def get_transfer_by_id(self, transfer_id: int) -> Transfer:
        stmt = "SELECT * FROM transfers WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, transfer_id)

        if row:
            return TransferDatabaseMapper.from_db_row(row)

        raise NotFoundError("Transfer with id = {transfer_id} not found")

    async def get_transfers_by_account_id(self, account_id: int) -> list[Transfer]:
        stmt = "SELECT * FROM transfers WHERE from_account_id = $1 OR to_account_id = $1"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt, account_id)

        return [TransferDatabaseMapper.from_db_row(row) for row in rows]
