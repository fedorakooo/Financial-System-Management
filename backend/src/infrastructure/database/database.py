import asyncpg
from typing import Optional

from src.config import settings

DATABASE_URL = settings.db.url


class DatabaseConnection:
    """Singleton class for managing the connection to a PostgreSQL database using asyncpg."""

    _instance: Optional["DatabaseConnection"] = None
    _pool: Optional[asyncpg.Pool] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._pool = None
        return cls._instance

    async def connect(self):
        """Establish a connection to the database."""
        if self._pool:
            raise ValueError("Already connected to the database.")
        try:
            self._pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the database: {e}")

    async def close(self):
        """Close the database connection."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def execute(self, query: str, *args):
        """Execute a SQL query that doesn't return any results."""
        if self._pool is None:
            raise ValueError("Not connected to the database. Call `await connect()` first.")
        async with self._pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        """Execute a query and return all rows from the result."""
        if self._pool is None:
            raise ValueError("Not connected to the database. Call `await connect()` first.")
        async with self._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """Execute a query and return a single row from the result."""
        if self._pool is None:
            raise ValueError("Not connected to the database. Call `await connect()` first.")
        async with self._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        """Execute a query and return a single value."""
        if self._pool is None:
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
