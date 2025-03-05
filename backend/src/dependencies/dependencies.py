from src.infrastructure.database.database import DatabaseConnection
from src.infrastructure.database.uow import UnitOfWork


class Dependencies:
    @staticmethod
    def get_database_connection() -> DatabaseConnection:
        return DatabaseConnection()

    @staticmethod
    def get_unit_of_work() -> UnitOfWork:
        return UnitOfWork.get_unit_of_work()
