from typing import List

from src.domain.abstractions.repositories.enterprises import AbstractEnterpriseRepository
from src.domain.abstractions.uow import AbstractUnitOfWork
from src.domain.schemas.enterprise import EnterpriseUpdate, EnterpriseRead, EnterpriseCreate


class EnterpriseService:
    def __init__(self, repository: AbstractEnterpriseRepository, uow: AbstractUnitOfWork):
        self.uow = uow
        self.repository = repository

    async def get_enterprise_by_id(self, enterprise_id: int) -> EnterpriseRead:
        enterprise = await self.repository.get_enterprise_by_id(enterprise_id)
        return enterprise

    async def get_enterprises(self) -> List[EnterpriseRead]:
        enterprises = await self.repository.get_enterprises()
        return enterprises

    async def create_enterprise(self, enterprise_create: EnterpriseCreate) -> EnterpriseRead:
        async with self.uow as uow:
            new_enterprise = await self.repository.create_enterprise(enterprise_create)
        return new_enterprise

    async def update_enterprise_by_id(self, enterprise_id: int, enterprise_update: EnterpriseUpdate) -> EnterpriseRead:
        async with self.uow as uow:
            updated_enterprise = await self.repository.update_enterprise_by_id(enterprise_id, enterprise_update)
        return updated_enterprise

    async def delete_enterprise_by_id(self, enterprise_id: int) -> None:
        async with self.uow as uow:
            await self.repository.delete_enterprise_by_id(enterprise_id)
