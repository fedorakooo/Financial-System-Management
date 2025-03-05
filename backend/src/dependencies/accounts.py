from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.infrastructure.database.database import DatabaseConnection
from src.infrastructure.database.repositories.account import AccountRepository
from src.infrastructure.database.uow import UnitOfWork
from src.services.accounts.account import AccountService


class AccountDependencies:
    @staticmethod
    def get_account_repository(
            db_connection: DatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> AccountRepository:
        return AccountRepository(db_connection)

    @staticmethod
    def get_account_service(
            repository: AccountRepository = Depends(get_account_repository),
            uow: UnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> AccountRepository:
        return AccountService(repository, uow)
