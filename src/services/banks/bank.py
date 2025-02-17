from typing import List, Optional

from src.domain.abstractions.repository import AbstractRepository
from src.domain.schemas.bank import BankCreate, BankRead, BankUpdate
from src.domain.abstractions.uow import AbstractUnitOfWork


class BankService:
    def __init__(self, repository: AbstractRepository, uow: AbstractUnitOfWork):
        self.uow = uow
        self.repository = repository

    async def create_bank(self, bank_create: BankCreate) -> BankRead:
        async with self.uow as uow:
            new_bank = await self.repository.add_one(bank_create)
        return new_bank

    async def get_all_banks(self) -> List[BankRead]:
        banks = await self.repository.find_all()
        return banks

    async def get_bank_by_id(self, id: int) -> Optional[BankRead]:
        bank = await self.repository.find_by_id(id=id)
        return bank

    async def update_bank_by_id(self, id: int, bank_update: BankUpdate) -> BankRead:
        async with self.uow as uow:
            await self.repository.update_one(id, bank_update)
        updated_bank = await self.repository.find_by_id(id)
        return updated_bank

    async def delete_bank(self, id: int) -> None:
        async with self.uow as uow:
            await self.repository.delete_one(id)
