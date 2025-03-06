from fastapi import Depends

from src.dependencies.logs import LogDependencies
from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.domain.abstractions.logger.logger import AbstractLogger
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.uow import UnitOfWork


class Dependencies:
    @staticmethod
    def get_database_connection(
            logger: AbstractLogger = Depends(LogDependencies.get_logger)
    ) -> AbstractDatabaseConnection:
        return DatabaseConnection(logger)

    @staticmethod
    def get_unit_of_work() -> AbstractUnitOfWork:
        return UnitOfWork.get_unit_of_work()
