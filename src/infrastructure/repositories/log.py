from src.domain.schemas.log import LogBase
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.logs import LogORM


class LogRepository(SQLAlchemyRepository[LogBase]):
    model = LogORM
