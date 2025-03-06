from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.infrastructure.database.repositories.user import UserRepository
from src.services.users.user import UserService


class UserDependencies:
    @staticmethod
    def get_user_repository(
            db_connection: AbstractDatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> AbstractUserRepository:
        return UserRepository(db_connection)

    @staticmethod
    def get_user_service(
            repository: AbstractUserRepository = Depends(get_user_repository),
            uow: AbstractUnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> UserService:
        return UserService(repository, uow)
