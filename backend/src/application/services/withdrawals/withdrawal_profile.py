from src.application.abstractions.withdrawals.withdrawal_profile import AbstractWithdrawalProfileService
from src.application.dtos.withdrawal import WithdrawalReadDTO, WithdrawalCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.withdrawal import WithdrawalMapper
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.withdrawal_manager import AbstractWithdrawalManagerRepository
from src.domain.abstractions.database.repositories.withdrawals import AbstractWithdrawalRepository
from src.application.services.withdrawals.access_control import WithdrawalProfileAccessControlService as AccessControl
from src.domain.exceptions.account import InsufficientFundsError


class WithdrawalProfileService(AbstractWithdrawalProfileService):
    def __init__(
            self,
            repository: AbstractWithdrawalRepository,
            account_repository: AbstractAccountRepository,
            manager_repository: AbstractWithdrawalManagerRepository
    ) -> None:
        self.repository = repository
        self.account_repository = account_repository
        self.manager_repository = manager_repository

    async def get_withdrawals_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[WithdrawalReadDTO]:
        account = await self.account_repository.get_account_by_id(account_id)
        AccessControl.can_get_withdrawals(account.user_id, requesting_user)

        withdrawals = await self.repository.get_withdrawals_by_account_id(account_id)

        withdrawals_dto = [WithdrawalMapper.map_withdrawal_to_withdrawal_read_dto(withdrawal) for withdrawal in withdrawals]
        return withdrawals_dto

    async def create_withdrawal(
            self,
            account_id: int,
            withdrawal_create_dto: WithdrawalCreateDTO,
            requesting_user: UserAccessDTO
    ) -> WithdrawalReadDTO:
        account = await self.account_repository.get_account_by_id(account_id)
        AccessControl.can_create_withdrawal(account.user_id, requesting_user)

        new_account_balance = account.balance - withdrawal_create_dto.amount
        if new_account_balance < 0:
            raise InsufficientFundsError(account.balance)

        created_withdrawal = self.manager_repository.create_withdrawal_with_balance_updates(withdrawal_create_dto, new_account_balance)

        created_withdrawal_dto = WithdrawalMapper.map_withdrawal_to_withdrawal_read_dto(created_withdrawal)
        return created_withdrawal_dto
