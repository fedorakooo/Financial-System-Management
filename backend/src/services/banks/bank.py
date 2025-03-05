from typing import List

from src.domain.abstractions.repositories.banks import AbstractBankRepository
from src.domain.schemas.bank import BankCreate, BankRead, BankUpdate
from src.domain.abstractions.uow import AbstractUnitOfWork


class BankService:
    def __init__(self, repository: AbstractBankRepository, uow: AbstractUnitOfWork):
        self.uow = uow
        self.repository = repository

    async def get_bank_by_id(self, bank_id: int) -> BankRead:
        bank = await self.repository.get_bank_by_id(bank_id)
        return bank

    async def get_banks(self) -> List[BankRead]:
        banks = await self.repository.get_banks()
        return banks

    async def create_bank(self, bank_create: BankCreate) -> BankRead:
        async with self.uow as uow:
            new_bank = await self.repository.create_bank(bank_create)
        return new_bank

    async def update_bank_by_id(self, bank_id: int, bank_update: BankUpdate) -> BankRead:
        async with self.uow as uow:
            updated_bank = await self.repository.update_bank_by_id(bank_id, bank_update)
        return updated_bank

    async def delete_bank_by_id(self, bank_id: int) -> None:
        async with self.uow as uow:
            await self.repository.delete_bank_by_id(bank_id)
