from src.application.abstractions.transfers.transfer_profile import AbstractTransferProfileService
from src.application.dtos.transfer import TransferReadDTO, TransferCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.transfer import TransferMapper
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.transfer import AbstractTransferRepository
from src.domain.abstractions.database.repositories.transfer_manager import AbstractTransferManagerRepository
from src.application.services.transfer.access_control import TransferProfileAccessControlService as AccessControl


class TransferProfileService(AbstractTransferProfileService):
    def __init__(
            self,
            repository: AbstractTransferRepository,
            account_repository: AbstractAccountRepository,
            manager_repository: AbstractTransferManagerRepository
    ) -> None:
        self.repository = repository
        self.account_repository = account_repository
        self.manager_repository = manager_repository

    async def get_transfers_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[TransferReadDTO]:
        account = await self.account_repository.get_account_by_id(account_id)
        AccessControl.can_get_transfers(account.user_id, requesting_user)

        transfers = await self.repository.get_transfers_by_account_id(account_id)

        transfers_dto = [TransferMapper.map_transfer_to_transfer_read_dto(transfer) for transfer in transfers]
        return transfers_dto

    async def create_transfer(
            self,
            transfer_create_dto: TransferCreateDTO,
            requesting_user: UserAccessDTO
    ) -> TransferReadDTO:
        sender_account = await self.account_repository.get_account_by_id(transfer_create_dto.from_account_id)
        AccessControl.can_create_transfer(sender_account.user_id, requesting_user)
        receive_account = await self.account_repository.get_account_by_id(transfer_create_dto.to_account_id)

        new_sender_account_balance = sender_account.balance - transfer_create_dto.amount
        new_receiver_account_balance = receive_account.balance + transfer_create_dto.amount

        transfer_create = TransferMapper.map_transfer_create_dto_to_transfer(transfer_create_dto)
        created_transfer = await self.manager_repository.create_transfer_with_balance_updates(
            transfer_create,
            new_sender_account_balance,
            new_receiver_account_balance
        )

        created_transfer_dto = TransferMapper.map_transfer_to_transfer_read_dto(created_transfer)
        return created_transfer_dto
