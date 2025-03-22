from src.application.abstractions.additions.addition_profile import AbstractAdditionProfileService
from src.application.dtos.addition import AdditionReadDTO, AdditionCreateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.addition import AdditionMapper
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.addition_manager import AbstractAdditionManagerRepository
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.application.services.additions.access_control import AdditionProfileAccessControlService as AccessControl


class AdditionProfileService(AbstractAdditionProfileService):
    def __init__(
            self,
            repository: AbstractAdditionRepository,
            account_repository: AbstractAccountRepository,
            manager_repository: AbstractAdditionManagerRepository
    ) -> None:
        self.repository = repository
        self.account_repository = account_repository
        self.manager_repository = manager_repository

    async def get_additions_by_account_id(
            self,
            account_id: int,
            requesting_user: UserAccessDTO
    ) -> list[AdditionReadDTO]:
        account = await self.account_repository.get_account_by_id(account_id)
        AccessControl.can_get_additions(account.user_id, requesting_user)

        additions = await self.repository.get_additions_by_account_id(account_id)

        additions_dto = [AdditionMapper.map_addition_to_addition_read_dto(addition) for addition in additions]
        return additions_dto

    async def create_addition(
            self,
            account_id: int,
            addition_create_dto: AdditionCreateDTO,
            requesting_user: UserAccessDTO
    ) -> AdditionReadDTO:
        account = await self.account_repository.get_account_by_id(account_id)
        AccessControl.can_create_addition(account.user_id, requesting_user)

        new_account_balance = account.balance + addition_create_dto.amount
        addition_create = AdditionMapper.map_addition_create_dto_to_addition(addition_create_dto, account_id)
        created_addition = await self.manager_repository.create_addition_with_balance_updates(addition_create,
                                                                                              new_account_balance)

        created_addition_dto = AdditionMapper.map_addition_to_addition_read_dto(created_addition)
        return created_addition_dto
