from dependency_injector import containers, providers

from src.infrastructure.database.repositories.account import AccountRepository
from src.infrastructure.database.repositories.addition import AdditionRepository
from src.infrastructure.database.repositories.bank import BankRepository
from src.infrastructure.database.repositories.user import UserRepository


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()

    gateways = providers.DependenciesContainer()

    bank_repository = providers.Factory(
        BankRepository,
        db_connection=gateways.database_connection,
    )

    user_repository = providers.Factory(
        UserRepository,
        db_connection=gateways.database_connection,
    )

    account_repository = providers.Factory(
        AccountRepository,
        db_connection=gateways.database_connection,
    )

    addition_repository = providers.Factory(
        AdditionRepository,
        db_connection=gateways.database_connection,
    )
