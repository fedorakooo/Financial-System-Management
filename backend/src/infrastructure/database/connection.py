import asyncpg

from src.config import settings
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.logger.logger import AbstractLogger
from src.infrastructure.logger.logger import Logger

DATABASE_URL = settings.db.url


class DatabaseConnection(AbstractDatabaseConnection):
    """Class for managing the connection to a PostgreSQL database using asyncpg."""

    def __init__(
            self,
            dsn: str,
            logger: AbstractLogger
    ):
        self.dsn = dsn
        self.logger = logger
        self._connection = None

    async def connect(self):
        self._connection = await asyncpg.connect(self.dsn)

    async def close(self):
        if self.connection:
            await self.connection.close()

    @property
    def connection(self):
        if not self._connection:
            raise RuntimeError("Database connection has not been established. Call 'connect()' first.")
        return self._connection

    async def execute(self, query: str, *args):
        return await self.connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        return await self.connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        return await self.connection.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        return await self.connection.fetchval(query, *args)

    async def __aenter__(self):
        """Set up the context manager by establishing a connection."""
        await self.connect()
        return self

    async def __aenter__(self):
        """Set up the context manager by establishing a connection and starting a transaction."""
        await self.connect()
        self._transaction = self.connection.transaction()  # Создаем транзакцию
        await self._transaction.start()  # Начинаем транзакцию
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Clean up by committing or rolling back the transaction and closing the connection."""
        if self._transaction:
            if exc_type is None:
                await self._transaction.commit()
            else:
                await self._transaction.rollback()
            self._transaction = None
        await self.close()
