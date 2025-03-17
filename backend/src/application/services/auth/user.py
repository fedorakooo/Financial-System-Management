from src.application.mappers.user import UserMapper
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.application.dtos.user import UserReadDTO


class AuthUserService:
    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    async def get_user_by_phone_number(self, phone_number: str) -> UserReadDTO:
        user = await self.repository.get_user_by_phone_number(phone_number)
        user_dto = UserMapper.map_user_to_user_read_dto(user)
        return user_dto

    async def get_user_hashed_password_by_phone_number(self, phone_number: str) -> str:
        hashed_password: str = await self.repository.get_user_hashed_password_by_phone_number(phone_number)
        return hashed_password
