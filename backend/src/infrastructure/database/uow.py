from typing import Optional
import asyncpg

from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.infrastructure.database.connection import DATABASE_URL


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.dsn = DATABASE_URL
        self.transaction: Optional[asyncpg.transaction.Transaction] = None

    async def __aenter__(self):
        self.connection = await asyncpg.connect(self.dsn)
        self.transaction = self.connection.transaction()
        await self.transaction.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.rollback()
        else:
            await self.commit()

        if self.connection:
            await self.connection.close()

    async def commit(self):
        if self.transaction:
            await self.transaction.commit()

    async def rollback(self):
        if self.transaction:
            await self.transaction.rollback()

    @classmethod
    def get_unit_of_work(cls) -> 'UnitOfWork':
        """Factory method to return a new UnitOfWork instance."""
        return cls()
