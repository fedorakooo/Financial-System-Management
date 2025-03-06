from typing import List

from src.domain.abstractions.logger.logger import AbstractLogger
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.exceptions.forbidden import ForbiddenError
from src.domain.schemas.account import AccountCreate, AccountRead, AccountCreateRequest
from src.domain.abstractions.database.uow import AbstractUnitOfWork


class AccountService:
    def __init__(self, repository: AbstractAccountRepository, uow: AbstractUnitOfWork):
        self.uow = uow
        self.repository = repository

    async def get_accounts_by_user_id(self, user_id: int) -> List[AccountRead]:
        accounts = await self.repository.get_accounts_by_user_id(user_id)
        return accounts

    async def create_account(
            self,
            account_create_request: AccountCreateRequest,
            user_id: int
    ) -> AccountRead:
        account_create_data = account_create_request.dict()
        account_create = AccountCreate(**account_create_data, user_id=user_id)

        async with self.uow as uow:
            created_account = await self.repository.create_account(account_create)

        return created_account

    async def delete_account_by_id(self, account_id: int, user_id: int) -> None:
        async with self.uow as uow:
            account: AccountRead = await self.repository.get_accounts_by_user_id(account_id)

            if account.user_id != user_id:
                raise ForbiddenError()

            await self.repository.delete_account_by_id(account_id)
