from typing import List

from src.application.abstractions.accounts.account_profile import AbstractAccountProfileService
from src.application.dtos.account import AccountReadDTO, AccountCreateDTO, AccountUpdateClientDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.account import AccountMapper
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.application.services.accounts.access_control import AccountProfileAccessControlService as AccessControl


class AccountProfileService(AbstractAccountProfileService):
    def __init__(
            self,
            repository: AbstractAccountRepository
    ):
        self.repository = repository

    async def get_account_by_id(self, account_id: int, requesting_user: UserAccessDTO) -> AccountReadDTO:
        account = await self.repository.get_account_by_id(account_id)
        AccessControl.can_get_account(account.user_id, requesting_user)
        account_dto = AccountMapper.map_account_to_account_read_dto(account)
        return account_dto

    async def get_accounts(self, requesting_user: UserAccessDTO) -> List[AccountReadDTO]:
        AccessControl.can_get_accounts(requesting_user)
        accounts = await self.repository.get_accounts_by_user_id(requesting_user.id)
        accounts_dto = [AccountMapper.map_account_to_account_read_dto(account) for account in accounts]
        return accounts_dto

    async def create_account(
            self,
            account_create_dto: AccountCreateDTO,
            requesting_user: UserAccessDTO
    ) -> AccountReadDTO:
        AccessControl.can_create_account(requesting_user)
        account_create = AccountMapper.map_account_create_dto_to_account(account_create_dto, requesting_user.id)
        created_account = await self.repository.create_account(account_create)
        created_account_dto = AccountMapper.map_account_to_account_read_dto(created_account)
        return created_account_dto

    async def update_account(
            self,
            account_id: int,
            account_update_dto: AccountUpdateClientDTO,
            requesting_user: UserAccessDTO
    ) -> AccountReadDTO:
        current_account = await self.repository.get_account_by_id(account_id)
        AccessControl.can_update_account(current_account.user_id, requesting_user)
        account_update = AccountMapper.map_account_update_client_dto_to_account(account_update_dto, current_account)
        updated_account = await self.repository.update_account(account_id, account_update)
        updated_account_dto = AccountMapper.map_account_to_account_read_dto(updated_account)
        return updated_account_dto
