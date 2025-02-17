import asyncpg
from typing import Optional

from src.infrastructure.config import settings

DATABASE_URL = settings.db.url


class DatabaseConnection:
    """Class for managing the connection to a PostgreSQL database using asyncpg."""

    def __init__(self):
        """Initialize the database connection with the DSN (Data Source Name)."""
        self.dsn = DATABASE_URL
        self.connection: Optional[asyncpg.Connection] = None

    async def connect(self):
        """Establish a connection to the database."""
        if self.connection is not None:
            raise ValueError("Already connected to the database.")
        try:
            self.connection = await asyncpg.connect(self.dsn)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the database: {e}")

    async def close(self):
        """Close the database connection."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def execute(self, query: str, *args):
        """Execute a SQL query that doesn't return any results."""
        if self.connection is None:
            raise ValueError("Not connected to the database.")
        return await self.connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        """Execute a query and return all rows from the result."""
        if self.connection is None:
            raise ValueError("Not connected to the database.")
        return await self.connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """Execute a query and return a single row from the result."""
        if self.connection is None:
            raise ValueError("Not connected to the database.")
        return await self.connection.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        """Execute a query and return a single value."""
        if self.connection is None:
            raise ValueError("Not connected to the database.")
        return await self.connection.fetchval(query, *args)

    async def __aenter__(self):
        """Set up the context manager by establishing a connection."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Clean up by closing the connection when exiting the context."""
        await self.close()
