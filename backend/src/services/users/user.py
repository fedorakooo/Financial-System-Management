from typing import List, Optional

from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.domain.schemas.user import UserCreate, UserRead, UserUpdate
from src.domain.utils.password import PasswordHandler


class UserService:
    def __init__(self, repository: AbstractUserRepository, uow: AbstractUnitOfWork):
        self.uow = uow
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> UserRead:
        user_create.hashed_password = PasswordHandler.hash_password(user_create.hashed_password)
        async with self.uow as uow:
            new_user = await self.repository.create_user(user_create)
        return new_user

    async def get_all_users(self) -> List[UserRead]:
        users = await self.repository.get_users()
        return users

    async def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        user = await self.repository.get_user_by_id(user_id)
        return user

    async def get_user_by_phone_number(self, phone_number: str) -> Optional[UserRead]:
        user = await self.repository.get_user_by_phone_number(phone_number)
        return user

    async def get_users_hashed_password_by_phone_number(
            self,
            phone_number: str
    ) -> str:
        hashed_password: str = await self.repository.get_user_hashed_password_by_phone_number(phone_number)
        return hashed_password

    async def update_user_by_id(self, user_id: int, user_update: UserUpdate) -> UserRead:
        async with self.uow as uow:
            updated_user = await self.repository.update_user_by_id(user_id, user_update)
        return updated_user

    async def delete_user_by_id(self, user_id: int) -> None:
        async with self.uow as uow:
            await self.repository.delete_user_by_id(user_id)
