from fastapi import Depends

from src.dependencies.dependencies import Dependencies
from src.infrastructure.database.database import DatabaseConnection
from src.infrastructure.database.repositories.enterprise import EnterpriseRepository
from src.infrastructure.database.uow import UnitOfWork
from src.services.enterprises.enterprise import EnterpriseService


class EnterpriseDependencies:
    @staticmethod
    def get_enterprise_repository(
            db_connection: DatabaseConnection = Depends(Dependencies.get_database_connection)
    ) -> EnterpriseRepository:
        return EnterpriseRepository(db_connection)

    @staticmethod
    def get_enterprise_service(
            repository: EnterpriseRepository = Depends(get_enterprise_repository),
            uow: UnitOfWork = Depends(Dependencies.get_unit_of_work)
    ) -> EnterpriseService:
        return EnterpriseService(repository, uow)
