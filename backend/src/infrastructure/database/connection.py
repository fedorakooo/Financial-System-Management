import asyncpg
from typing import Optional

from src.config import settings
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.logger.logger import AbstractLogger
from src.infrastructure.logger.logger import Logger

DATABASE_URL = settings.db.url


class DatabaseConnection(AbstractDatabaseConnection):
    """Singleton class for managing the connection to a PostgreSQL database using asyncpg."""

    _instance: Optional["DatabaseConnection"] = None
    _pool: Optional[asyncpg.Pool] = None
    logger: AbstractLogger

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._pool = None
        return cls._instance

    def __init__(self, logger=Optional[Logger]):
        self.logger = logger or Logger()

    async def connect(self):
        if self._pool:
            self.logger.warning("Attempted to connect while already connected to the database.")
            raise ValueError("Already connected to the database.")
        try:
            self._pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        except Exception as e:
            self.logger.error(f"Failed to connect to the database: {str(e)}")
            raise ConnectionError(f"Failed to connect to the database")

    async def close(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def execute(self, query: str, *args):
        if self._pool is None:
            self.logger.error("Not connected to the database. Call `await connect()` first.")
            raise ValueError("Not connected to the database. Call `await connect()` first.")
        async with self._pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        if self._pool is None:
            self.logger.error("Not connected to the database. Call `await connect()` first.")
            raise ValueError("Not connected to the database. Call `await connect()` first.")
        async with self._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        if self._pool is None:
            self.logger.error("Not connected to the database. Call `await connect()` first.")
            raise ValueError("Not connected to the database. Call `await connect()` first.")
        async with self._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        if self._pool is None:
            self.logger.error("Not connected to the database. Call `await connect()` first.")
            raise ValueError("Not connected to the database. Call `await connect()` first.")
        async with self._pool.acquire() as connection:
            return await connection.fetchval(query, *args)

    async def __aenter__(self):
        """Set up the context manager by establishing a connection."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Clean up by closing the connection when exiting the context."""
        await self.close()
