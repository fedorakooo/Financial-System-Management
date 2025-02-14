from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.loans import LoanORM


class LoanRepository(SQLAlchemyRepository):
    model = LoanORM
