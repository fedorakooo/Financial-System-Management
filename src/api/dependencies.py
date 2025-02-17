from fastapi import Depends

from src.infrastructure.repositories.bank import BankRepository
from src.infrastructure.uow import UnitOfWork
from src.services.banks.bank import BankService


def get_bank_repository() -> BankRepository:
    return BankRepository()


def get_bank_service(
        repository: BankRepository = Depends(get_bank_repository),
        uow: UnitOfWork = Depends(UnitOfWork.get_unit_of_work)
) -> BankService:
    return BankService(repository, uow)
