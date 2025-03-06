from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.infrastructure.database.repositories.account import AccountRepository
from src.services.accounts.account import AccountService


class AccountDependencies:
    @staticmethod
    def get_account_repository(
            db_connection: AbstractDatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> AbstractAccountRepository:
        return AccountRepository(db_connection)

    @staticmethod
    def get_account_service(
            repository: AbstractAccountRepository = Depends(get_account_repository),
            uow: AbstractUnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> AccountService:
        return AccountService(repository, uow)
