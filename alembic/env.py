import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from alembic import context

from src.infrastructure.database import DATABASE_URL, Base

from src.infrastructure.models.accounts import AccountORM
from src.infrastructure.models.banks import BankORM
from src.infrastructure.models.enterprises import EnterpriseORM
from src.infrastructure.models.installments import InstallmentORM
from src.infrastructure.models.loans import LoanORM
from src.infrastructure.models.logs import LogORM
from src.infrastructure.models.payroll import PayrollRequestORM
from src.infrastructure.models.transactions import TransactionORM
from src.infrastructure.models.users import UserORM

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config

config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = create_async_engine(DATABASE_URL, echo=True)

    async_sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            literal_binds=True,
        )

        async with connection.begin():
            await context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
