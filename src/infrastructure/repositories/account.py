from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.accounts import AccountORM


class AccountRepository(SQLAlchemyRepository):
    model = AccountORM
