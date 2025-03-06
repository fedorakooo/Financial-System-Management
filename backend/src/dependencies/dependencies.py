from src.domain.abstractions.database.connection import AbstractDatabaseConnection
from src.domain.abstractions.database.uow import AbstractUnitOfWork
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.uow import UnitOfWork


class Dependencies:
    @staticmethod
    def get_database_connection() -> AbstractDatabaseConnection:
        return DatabaseConnection()

    @staticmethod
    def get_unit_of_work() -> AbstractUnitOfWork:
        return UnitOfWork.get_unit_of_work()
