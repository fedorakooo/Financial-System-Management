from fastapi import Depends

from src.dependencies.accounts import AccountDependencies
from src.dependencies.dependencies import Dependencies
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.infrastructure.database.repositories.account import AccountRepository
from src.infrastructure.database.repositories.addition import AdditionRepository
from src.services.additions.addition import AdditionService


class AdditionsDependencies:
    @staticmethod
    def get_addition_repository(
            db_connection: AbstractDatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> AbstractAdditionRepository:
        return AdditionRepository(db_connection)

    @staticmethod
    def get_addition_service(
            repository: AbstractAdditionRepository = Depends(get_addition_repository),
            uow: AbstractUnitOfWork = Depends(Dependencies.get_unit_of_work),
            account_repository: AccountRepository = Depends(AccountDependencies.get_account_repository)
    ) -> AdditionService:
        return AdditionService(repository, uow, account_repository)
