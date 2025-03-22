from dependency_injector import containers, providers

from src.infrastructure.database.repositories.account import AccountRepository
from src.infrastructure.database.repositories.addition import AdditionRepository
from src.infrastructure.database.repositories.addition_manager import AdditionManagerRepository
from src.infrastructure.database.repositories.bank import BankRepository
from src.infrastructure.database.repositories.transfer import TransferRepository
from src.infrastructure.database.repositories.transfer_manager import TransferManagerRepository
from src.infrastructure.database.repositories.user import UserRepository
from src.infrastructure.database.repositories.withdrawal import WithdrawalRepository
from src.infrastructure.database.repositories.withdrawal_manager import WithdrawalManagerRepository


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

    withdrawal_repository = providers.Factory(
        WithdrawalRepository,
        db_connection=gateways.database_connection,
    )

    addition_manager_repository = providers.Factory(
        AdditionManagerRepository,
        db_connection=gateways.database_connection,
    )

    withdrawal_manager_repository = providers.Factory(
        WithdrawalManagerRepository,
        db_connection=gateways.database_connection,
    )

    transfer_repository = providers.Factory(
        TransferRepository,
        db_connection=gateways.database_connection,
    )

    transfer_manager_repository = providers.Factory(
        TransferManagerRepository,
        db_connection=gateways.database_connection,
    )