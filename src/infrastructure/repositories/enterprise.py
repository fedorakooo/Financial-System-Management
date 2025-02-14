from src.domain.schemas.enterprise import EnterpriseBase
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.enterprises import EnterpriseORM


class EnterpriseRepository(SQLAlchemyRepository[EnterpriseBase]):
    model = EnterpriseORM
