from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.entities.addition import Addition
from src.infrastructure.database.mappers.addition import AdditionDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class AdditionRepository(AbstractAdditionRepository):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection: AbstractDatabaseConnection = db_connection

    async def get_addition_by_id(self, addition_id: int) -> Addition:
        stmt = "SELECT * FROM additions WHERE id = $1"

        async with self.db_connection as conn:
            row = await conn.fetchrow(stmt, addition_id)

        if row:
            return AdditionDatabaseMapper.from_db_row(row)

        raise NotFoundError("Addition with id = {addition_id} not found")

    async def get_additions(self) -> list[Addition]:
        stmt = "SELECT * FROM additions"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt)

        return [AdditionDatabaseMapper.from_db_row(row) for row in rows]

    async def get_additions_by_account_id(self, account_id: int) -> list[Addition]:
        stmt = "SELECT * FROM additions WHERE account_id = $1"

        async with self.db_connection as conn:
            rows = await conn.fetch(stmt, account_id)

        return [AdditionDatabaseMapper.from_db_row(row) for row in rows]
