from src.domain.schemas.bank import BankRead
from src.infrastructure.database import DatabaseConnection
from src.infrastructure.models.banks import BankORM
from src.infrastructure.repositories.sql import SQLRepository


class BankRepository(SQLRepository[BankORM]):
    table_name = "banks"
    model_class = BankRead

    @classmethod
    async def create_table(cls) -> None:
        schema = """CREATE TABLE IF NOT EXISTS banks (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        bic VARCHAR(32) NOT NULL UNIQUE,
                        address VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );"""
        async with DatabaseConnection() as conn:
            await conn.execute(schema)
