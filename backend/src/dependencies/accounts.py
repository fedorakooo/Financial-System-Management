from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.repositories.account import AccountRepository
from src.infrastructure.database.uow import UnitOfWork
from src.services.accounts.account import AccountService


class AccountDependencies:
    @staticmethod
    def get_account_repository(
            db_connection: AbstractDatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> AbstractAccountRepository:
        return AccountRepository(db_connection)

    @staticmethod
    def get_account_service(
            repository: AccountRepository = Depends(get_account_repository),
            uow: UnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> AccountService:
        return AccountService(repository, uow)
