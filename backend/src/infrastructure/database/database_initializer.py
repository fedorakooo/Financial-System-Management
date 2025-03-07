from src.infrastructure.database.connection import DatabaseConnection


class DatabaseInitializer:
    @classmethod
    async def create_all_tables(cls) -> None:
        """Method to call the creation of all tables"""
        await cls.create_banks_table()
        await cls.create_users_table()
        await cls.create_enterprise_table()
        await cls.create_accounts_table()
        await cls.create_additions_table()

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
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_updated_at') THEN
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
        create_enum_role = """
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
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_user_updated_at') THEN
                    CREATE TRIGGER trigger_update_user_updated_at
                    BEFORE UPDATE ON users
                    FOR EACH ROW
                    EXECUTE FUNCTION update_user_updated_at();
                END IF;
            END $$;
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_enum_role)
            await conn.execute(create_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    @classmethod
    async def create_enterprise_table(cls) -> None:
        create_enum_type = """
            DO $$   
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'enterprise_type') THEN
                    CREATE TYPE enterprise_type AS ENUM ('LLC', 'SP', 'LLP');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS enterprises (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                type enterprise_type NOT NULL,
                unp VARCHAR(64) NOT NULL UNIQUE,
                bank_id INTEGER NOT NULL REFERENCES banks(id),
                address VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
        """

        create_function = """
            CREATE OR REPLACE FUNCTION update_enterprise_updated_at()
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
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_enterprise_updated_at') THEN
                    CREATE TRIGGER trigger_update_enterprise_updated_at
                    BEFORE UPDATE ON enterprises
                    FOR EACH ROW
                    EXECUTE FUNCTION update_enterprise_updated_at();
                END IF;
            END $$;
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_enum_type)
            await conn.execute(create_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    @classmethod
    async def create_accounts_table(cls) -> None:
        create_enum_status = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'account_status') THEN
                    CREATE TYPE account_status AS ENUM ('ACTIVE', 'BLOCKED', 'FROZEN');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS accounts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                enterprise_id INTEGER REFERENCES enterprises(id),
                bank_id INTEGER NOT NULL REFERENCES banks(id),
                balance DECIMAL(30,2) NOT NULL CHECK (balance > 0),
                status account_status NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
        """

        create_function = """
            CREATE OR REPLACE FUNCTION update_account_updated_at()
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
                IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_account_updated_at') THEN
                    CREATE TRIGGER trigger_update_account_updated_at
                    BEFORE UPDATE ON accounts
                    FOR EACH ROW
                    EXECUTE FUNCTION update_account_updated_at();
                END IF;
            END $$;
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_enum_status)
            await conn.execute(create_table)
            await conn.execute(create_function)
            await conn.execute(create_trigger)

    @classmethod
    async def create_additions_table(cls) -> None:
        create_enum_source = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'addition_source') THEN
                    CREATE TYPE addition_source AS ENUM ('BANK_TRANSFER', 'CARD_PAYMENT', 'CASH', 'CRYPTO', 'OTHER');
                END IF;
            END $$;
        """

        create_enum_status = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'addition_status') THEN
                    CREATE TYPE addition_status AS ENUM ('PENDING', 'COMPLETED', 'FAILED');
                END IF;
            END $$;
        """

        create_table = """
            CREATE TABLE IF NOT EXISTS additions (
                id SERIAL PRIMARY KEY,
                account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                amount DECIMAL(18,2) NOT NULL CHECK (amount > 0),
                source addition_source NOT NULL,
                status addition_status NOT NULL DEFAULT 'PENDING',
                created_at TIMESTAMP DEFAULT NOW() NOT NULL
            );
        """

        async with DatabaseConnection() as conn:
            await conn.execute(create_enum_source)
            await conn.execute(create_enum_status)
            await conn.execute(create_table)
