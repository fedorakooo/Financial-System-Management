from src.domain.schemas.installment import InstallmentBase
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.installments import InstallmentORM


class InstallmentRepository(SQLAlchemyRepository[InstallmentBase]):
    model = InstallmentORM
