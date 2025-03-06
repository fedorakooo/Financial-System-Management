from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.repositories.enterprises import AbstractEnterpriseRepository
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.infrastructure.database.repositories.enterprise import EnterpriseRepository
from src.services.enterprises.enterprise import EnterpriseService


class EnterpriseDependencies:
    @staticmethod
    def get_enterprise_repository(
            db_connection: AbstractDatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> AbstractEnterpriseRepository:
        return EnterpriseRepository(db_connection)

    @staticmethod
    def get_enterprise_service(
            repository: AbstractEnterpriseRepository = Depends(get_enterprise_repository),
            uow: AbstractUnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> EnterpriseService:
        return EnterpriseService(repository, uow)
