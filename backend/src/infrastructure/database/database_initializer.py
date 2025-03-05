from src.infrastructure.database.database import DatabaseConnection


class DatabaseInitializer:
    @classmethod
    async def create_all_tables(cls) -> None:
        """Method to call the creation of all tables"""
        await cls.create_banks_table()
        await cls.create_users_table()

    @classmethod
    async def create_banks_table(cls) -> None:
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

        create_index = "CREATE INDEX IF NOT EXISTS idx_banks_bic ON banks(bic);"

        create_function = """
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        create_trigger = """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_updated_at'
                ) THEN
                    CREATE TRIGGER trigger_update_updated_at
                    BEFORE UPDATE ON banks
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column();
                END IF;
            END $$;
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_table)
            await conn.execute(create_index)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    @classmethod
    async def create_users_table(cls) -> None:
        create_enum = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
                    CREATE TYPE user_role AS ENUM ('CLIENT', 'OPERATOR', 'MANAGER', 'ADMINISTRATOR', 'SPECIALIST');
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

        create_function = """
            CREATE OR REPLACE FUNCTION update_user_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = now();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """

        create_trigger = """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_user_updated_at'
                ) THEN
                    CREATE TRIGGER trigger_update_user_updated_at
                    BEFORE UPDATE ON users
                    FOR EACH ROW
                    EXECUTE FUNCTION update_user_updated_at();
                END IF;
            END $$;
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_enum)
            await conn.execute(create_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)
