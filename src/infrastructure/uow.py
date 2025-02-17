from typing import Optional
import asyncpg

from src.domain.abstractions.uow import AbstractUnitOfWork
from src.infrastructure.database import DATABASE_URL


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.dsn = DATABASE_URL
        self.connection: Optional[asyncpg.Connection] = None

    async def __aenter__(self):
        self.connection = await asyncpg.connect(self.dsn)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.connection:
            await self.connection.close()

    async def commit(self):
        if self.connection:
            await self.connection.execute("COMMIT")

    async def rollback(self):
        if self.connection:
            await self.connection.execute("ROLLBACK")

    @classmethod
    def get_unit_of_work(cls) -> 'UnitOfWork':
        """Factory method to return a new UnitOfWork instance."""
        return cls()
