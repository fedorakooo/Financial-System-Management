from typing import List

from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.domain.schemas.addition import AdditionRead, AdditionCreate


class AdditionService:
    def __init__(
            self,
            repository: AbstractAdditionRepository,
            uow: AbstractUnitOfWork,
            account_repository: AbstractAccountRepository
    ):
        self.uow: AbstractUnitOfWork = uow
        self.repository: AbstractAdditionRepository = repository
        self.account_repository: AbstractAccountRepository = account_repository

    async def get_addition_by_id(self, addition_id: int) -> AdditionRead:
        addition = await self.repository.get_addition_by_id(addition_id)
        return addition

    async def get_additions(self) -> List[AdditionRead]:
        additions = await self.repository.get_additions()
        return additions

    async def get_additions_by_account_id(self, account_id: int) -> List[AdditionRead]:
        additions = await self.repository.get_additions_by_account_id(account_id)
        return additions

    async def create_addition(self, addition_create_request: AdditionCreate, user_id: int) -> AdditionRead:
        addition_create_data = addition_create_request.dict()
        addition_create = AdditionCreate(**addition_create_data)

        async with self.uow as uow:
            created_addition = await self.repository.create_addition(addition_create)
            await self.account_repository.update_account_balance(
                addition_create.account_id,
                addition_create.amount
            )
        return created_addition
