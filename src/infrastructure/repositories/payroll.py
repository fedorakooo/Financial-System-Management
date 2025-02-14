from src.domain.schemas.payroll import PayrollRequestBase
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.payroll import PayrollRequestORM


class PayrollRequestRepository(SQLAlchemyRepository[PayrollRequestBase]):
    model = PayrollRequestORM
