from abc import abstractmethod, ABC
from decimal import Decimal

from cryptography.hazmat.primitives.keywrap import aes_key_unwrap_with_padding

from src.application.abstractions.loans.loan_management import AbstractLoanManagementService
from src.application.dtos.bank import BankReadDTO, BankCreateDTO, BankUpdateDTO
from src.application.dtos.loan import LoanAccountReadDTO, LoanTransactionReadDTO
from src.application.dtos.user import UserAccessDTO
from src.application.mappers.loan import LoanMapper
from src.domain.abstractions.database.uows.loan import AbstractLoanUnitOfWork
from src.domain.entities.loan import LoanTransaction
from src.domain.enums.loan import LoanAccountStatus, LoanTransactionType
from src.application.services.loans.access_control import LoanManagementAccessControlService as AccessControl
from src.domain.exceptions.loan import LoanAccountNotPendingError


class LoanManagementService(AbstractLoanManagementService):
    def __init__(self, uow: AbstractLoanUnitOfWork):
        self.uow = uow

    async def approve_loan_account_request(
            self,
            loan_account_id: int,
            requesting_user: UserAccessDTO
    ) -> LoanAccountReadDTO:
        async with self.uow as uow:
            AccessControl.can_approve_loan_request(requesting_user)
            loan_account = await self.uow.loan_repository.get_loan_account_by_id(loan_account_id)
            if loan_account.status is not LoanAccountStatus.PENDING:
                raise LoanAccountNotPendingError()
            await self.uow.loan_repository.update_loan_account_status_by_id(loan_account_id, LoanAccountStatus.ACTIVE)
            loan = await self.uow.loan_repository.get_loan_by_id(loan_account.loan_id)
            await self.uow.account_repository.update_account_balance(loan_account.account_id, loan.amount)
            updated_account = await self.uow.account_repository.get_account_by_id(loan_account.account_id)
            created_loan_transaction = await self.uow.loan_repository.create_loan_transaction(
                LoanTransaction(
                    loan_account_id=loan_account_id,
                    type=LoanTransactionType.CREDIT.value,
                    amount=loan.amount
                )
            )
        loan_account_dto = LoanMapper.map_loan_account_to_loan_account_read_dto(
            loan_account,
            updated_account,
            loan
        )
        return loan_account_dto
