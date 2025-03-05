from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.infrastructure.database.database import DatabaseConnection
from src.infrastructure.database.repositories.user import UserRepository
from src.infrastructure.database.uow import UnitOfWork
from src.services.users.user import UserService


class UserDependencies:
    @staticmethod
    def get_user_repository(
            db_connection: DatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> UserRepository:
        return UserRepository(db_connection)

    @staticmethod
    def get_user_service(
            repository: UserRepository = Depends(get_user_repository),
            uow: UnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> UserService:
        return UserService(repository, uow)
