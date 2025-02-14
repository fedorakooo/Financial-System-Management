from src.domain.schemas.user import UserBase
from src.infrastructure.repositories.sqlalchemy_repo import SQLAlchemyRepository
from src.infrastructure.models.users import UserORM


class UserRepository(SQLAlchemyRepository[UserBase]):
    model = UserORM
