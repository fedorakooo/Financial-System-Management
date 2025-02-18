from src.domain.schemas.bank import BankRead, BankBase
from src.infrastructure.database import DatabaseConnection
from src.infrastructure.repositories.sql import SQLRepository


class BankRepository(SQLRepository[BankBase]):
    table_name = "banks"
    model_class = BankRead

    @classmethod
    async def create_table(cls) -> None:
        create_table = """
            CREATE TABLE IF NOT EXISTS banks (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                bic VARCHAR(32) NOT NULL UNIQUE,
                address VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT now() NOT NULL,
                updated_at TIMESTAMP DEFAULT now() NOT NULL
            );
        """

        create_trigger = """
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_update_updated_at
            BEFORE UPDATE ON banks
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_table)
            await conn.execute(create_trigger)
