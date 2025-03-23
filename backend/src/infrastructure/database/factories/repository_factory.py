from src.domain.abstractions.database.factories.repository import AbstractRepositoryFactory
from src.domain.abstractions.database.repositories.accounts import AbstractAccountRepository
from src.domain.abstractions.database.repositories.additions import AbstractAdditionRepository
from src.domain.abstractions.database.repositories.banks import AbstractBankRepository
from src.domain.abstractions.database.repositories.transfer import AbstractTransferRepository
from src.domain.abstractions.database.repositories.users import AbstractUserRepository
from src.domain.abstractions.database.repositories.withdrawals import AbstractWithdrawalRepository
from src.infrastructure.database.repositories.account import AccountRepository
from src.infrastructure.database.repositories.addition import AdditionRepository
from src.infrastructure.database.repositories.bank import BankRepository
from src.infrastructure.database.repositories.transfer import TransferRepository
from src.infrastructure.database.repositories.user import UserRepository
from src.infrastructure.database.repositories.withdrawal import WithdrawalRepository


class RepositoryFactory(AbstractRepositoryFactory):
    def create_account_repository(self, connection) -> AbstractAccountRepository:
        return AccountRepository(connection)

    def create_addition_repository(self, connection) -> AbstractAdditionRepository:
        return AdditionRepository(connection)

    def create_bank_repository(self, connection) -> AbstractBankRepository:
        return BankRepository(connection)

    def create_transfer_repository(self, connection) -> AbstractTransferRepository:
        return TransferRepository(connection)

    def create_withdrawal_repository(self, connection) -> AbstractWithdrawalRepository:
        return WithdrawalRepository(connection)

    def create_user_repository(self, connection) -> AbstractUserRepository:
        return UserRepository(connection)
