from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.uow import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection = db_connection
        self.transaction = None

    async def __aenter__(self):
        await self.db_connection.connect()
        self.transaction = self.db_connection.connection.transaction()
        await self.transaction.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.transaction.commit()
        else:
            await self.transaction.rollback()
        await self.db_connection.close()

    async def commit(self):
        if self.transaction:
            await self.transaction.commit()

    async def rollback(self):
        if self.transaction:
            await self.transaction.rollback()
