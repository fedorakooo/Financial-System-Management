from src.domain.schemas.transaction import TransactionBase
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.transactions import TransactionORM


class UserRepository(SQLAlchemyRepository[TransactionBase]):
    model = TransactionORM
