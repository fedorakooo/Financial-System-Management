from typing import Optional

from src.application.dtos.profile import ProfileUpdateDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.profile import ProfileMapper
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.application.abstractions.profile.profile import AbstractProfileService
from src.domain.entities.user import User


class ProfileService(AbstractProfileService):
    def __init__(self, repository: AbstractUserRepository, uow: AbstractUnitOfWork):
        self.uow = uow
        self.repository = repository

    async def get_profile(self, requesting_user: UserAccessDTO) -> Optional[User]:
        user = await self.repository.get_user_by_id(requesting_user.id)
        profile_dto = ProfileMapper.map_user_to_profile_read_dto(user)
        return profile_dto

    async def update_profile_by_user_id(
            self,
            requesting_user: UserAccessDTO,
            profile_update_dto: ProfileUpdateDTO
    ) -> User:
        current_user = await self.repository.get_user_by_id(requesting_user.id)

        user_update = ProfileMapper.map_profile_update_dto_to_user(profile_update_dto, current_user)

        async with self.uow as uow:
            updated_user = await self.repository.update_user_by_id(requesting_user.id, user_update)

        updated_profile_dto = ProfileMapper.map_user_to_profile_read_dto(updated_user)
        return updated_profile_dto

    async def delete_user_by_id(self, requesting_user: UserAccessDTO) -> None:
        async with self.uow as uow:
            await self.repository.delete_user_by_id(requesting_user.id)
