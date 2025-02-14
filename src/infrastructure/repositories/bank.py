from src.domain.schemas.bank import BankBase
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.banks import BankORM


class BankRepository(SQLAlchemyRepository[BankBase]):
    model = BankORM
