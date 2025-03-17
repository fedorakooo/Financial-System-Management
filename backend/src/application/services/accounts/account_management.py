from typing import List

from src.application.abstractions.accounts.account_management import AbstractAccountManagementService
from src.application.dtos.account import AccountReadDTO, AccountUpdateStaffDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.account import AccountMapper
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.application.services.accounts.access_control import AccountManagementAccessControlService as AccessControl


class AccountManagementService(AbstractAccountManagementService):
    def __init__(
            self,
            repository: AbstractAccountRepository,
            uow: AbstractUnitOfWork,
    ):
        self.uow = uow
        self.repository = repository

    async def get_accounts_by_user_id(self, user_id: int, requesting_user: UserAccessDTO) -> List[AccountReadDTO]:
        AccessControl.can_get_accounts(requesting_user)
        accounts = await self.repository.get_accounts_by_user_id(user_id)
        accounts_dto = [AccountMapper.map_account_to_account_read_dto(account) for account in accounts]
        return accounts_dto

    async def update_account_by_id(
            self,
            account_id: int,
            account_update_dto: AccountUpdateStaffDTO,
            requesting_user: UserAccessDTO
    ) -> AccountReadDTO:
        AccessControl.can_update_account(requesting_user)

        current_account = await self.repository.get_account_by_id(account_id)

        account_update = AccountMapper.map_account_update_staff_dto_to_account(account_update_dto, current_account)

        async with self.uow as uow:
            updated_account = await self.repository.update_account(account_id, account_update)

        updated_account_dto = AccountMapper.map_account_to_account_read_dto(updated_account)
        return updated_account_dto

    async def delete_account_by_id(self, account_id: int, requesting_user: UserAccessDTO) -> None:
        AccessControl.can_delete_account(requesting_user)

        async with self.uow as uow:
            await self.repository.delete_account_by_id(account_id)
