from src.domain.schemas.user import UserBase, UserRead
from src.infrastructure.database import DatabaseConnection
from src.infrastructure.repositories.sql import SQLRepository


class UserRepository(SQLRepository[UserBase]):
    table_name = "users"
    model_class = UserRead

    @classmethod
    async def create_table(cls) -> None:
        create_enum = """
                    DO $$ 
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
                            CREATE TYPE user_role AS ENUM ('CLIENT', 'OPERATOR', 'MANAGER', 'ADMINISTRATOR');
                        END IF;
                    END $$;
                """

        create_table = """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        passport_number VARCHAR(20) NOT NULL UNIQUE,
                        phone_number VARCHAR(20) NOT NULL UNIQUE,
                        email VARCHAR(100) NOT NULL UNIQUE,
                        role user_role NOT NULL,
                        hashed_password TEXT NOT NULL,
                        is_active BOOLEAN NOT NULL DEFAULT FALSE,
                        is_foreign BOOLEAN NOT NULL DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                    );
                """

        create_trigger = """
            CREATE OR REPLACE FUNCTION update_user_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_update_user_updated_at
            BEFORE UPDATE ON users
            FOR EACH ROW
            EXECUTE FUNCTION update_user_updated_at();
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_enum)
            await conn.execute(create_table)
            await conn.execute(create_trigger)
