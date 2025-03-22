from src.application.abstractions.withdrawals.withdrawal_profile import AbstractWithdrawalProfileService
from src.application.dtos.withdrawal import WithdrawalReadDTO, WithdrawalCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.withdrawal import WithdrawalMapper
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.withdrawals import AbstractWithdrawalRepository
from src.application.services.withdrawals.access_control import WithdrawalProfileAccessControlService as AccessControl


class WithdrawalProfileService(AbstractWithdrawalProfileService):
    def __init__(
            self,
            repository: AbstractWithdrawalRepository,
            account_repository: AbstractAccountRepository
    ) -> None:
        self.repository = repository
        self.account_repository = account_repository

    async def get_withdrawals_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[WithdrawalReadDTO]:
        account = await self.account_repository.get_account_by_id(account_id)
        AccessControl.can_get_withdrawals(account.user_id, requesting_user)

        withdrawals = await self.repository.get_withdrawals_by_account_id(account_id)

        withdrawals_dto = [WithdrawalMapper.map_withdrawal_to_withdrawal_read_dto(withdrawal) for withdrawal in
                           withdrawals]
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
            raise Exception("Update it later")

        withdrawal_create = WithdrawalMapper.map_withdrawal_create_dto_to_withdrawal(withdrawal_create_dto, account_id)
        created_withdrawal = await self.repository.create_withdrawal(withdrawal_create)
        await self.account_repository.update_account_balance(account_id, new_account_balance)

        created_withdrawal_dto = WithdrawalMapper.map_withdrawal_to_withdrawal_read_dto(created_withdrawal)
        return created_withdrawal_dto
