from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.domain.abstractions.database.repositories.banks import AbstractBankRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.infrastructure.database.repositories.bank import BankRepository
from src.services.banks.bank import BankService


class BankDependencies:
    @staticmethod
    def get_bank_repository(
            db_connection: AbstractBankRepository = Depends(Dependencies.get_database_connection)
    ) -> AbstractBankRepository:
        return BankRepository(db_connection)

    @staticmethod
    def get_bank_service(
            repository: AbstractBankRepository = Depends(get_bank_repository),
            uow: AbstractUnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> BankService:
        return BankService(repository, uow)
