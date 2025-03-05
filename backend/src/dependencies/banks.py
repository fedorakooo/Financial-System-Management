from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.infrastructure.database.database import DatabaseConnection
from src.infrastructure.database.repositories.bank import BankRepository
from src.infrastructure.database.uow import UnitOfWork
from src.services.banks.bank import BankService


class BankDependencies:
    @staticmethod
    def get_bank_repository(
            db_connection: DatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> BankRepository:
        return BankRepository(db_connection)

    @staticmethod
    def get_bank_service(
            repository: BankRepository = Depends(get_bank_repository),
            uow: UnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> BankService:
        return BankService(repository, uow)
