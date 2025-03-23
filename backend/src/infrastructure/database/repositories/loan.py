from typing import Any

from src.domain.abstractions.database.repositories.loans import AbstractLoanRepository
from src.domain.entities.loan import Loan, LoanTransaction, LoanAccount
from src.infrastructure.database.mappers.loan import LoanDatabaseMapper
from src.infrastructure.exceptions.repository_exceptions import NotFoundError


class LoanRepository(AbstractLoanRepository):
    def __init__(self, connection: Any):
        self.connection = connection

    async def get_loan_by_id(self, loan_id: int) -> Loan:
        stmt = "SELECT * FROM loans WHERE id = $1"
        row = await self.connection.fetchrow(stmt, loan_id)
        if row is None:
            raise NotFoundError(f"Loan with id = {loan_id} not found")
        return LoanDatabaseMapper.from_db_row_to_loan(row)

    async def get_loan_transactions_by_loan_account_id(self, loan_account_id: int) -> list[LoanTransaction]:
        stmt = "SELECT * FROM loan_transactions WHERE loan_account_id = $1"
        rows = await self.connection.fetch(stmt, loan_account_id)
        return [LoanDatabaseMapper.from_db_row_to_loan_transaction(row) for row in rows]

    async def get_loan_account_by_id(self, loan_account_id: int) -> LoanAccount:
        stmt = "SELECT * FROM loan_accounts WHERE loan_account_id = $1"
        row = await self.connection.fetchrow(stmt, loan_account_id)
        if row is None:
            raise NotFoundError(f"Loan account with id = {loan_account_id} not found")
        return LoanDatabaseMapper.from_db_row_to_loan_account(row)

    async def get_loan_accounts_by_user_id(self, user_id: int) -> list[LoanAccount]:
        stmt = "SELECT * FROM loan_accounts WHERE user_id = $1"
        row = await self.connection.fetchrow(stmt, user_id)
        return LoanDatabaseMapper.from_db_row_to_loan_account(row)

    async def create_loan(self, loan: Loan) -> Loan:
        loan_create_row = LoanDatabaseMapper.from_loan_to_db_row(loan)
        columns = ', '.join(loan_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(loan_create_row))])
        values = tuple(loan_create_row.values())

        stmt = f"INSERT INTO loans ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return LoanDatabaseMapper.from_db_row_to_loan(row)

    async def create_loan_transaction(self, loan_transaction: LoanTransaction) -> LoanTransaction:
        loan_transaction_create_row = LoanDatabaseMapper.from_loan_to_db_row(loan_transaction)
        columns = ', '.join(loan_transaction_create_row.keys())
        placeholders = ', '.join([f"${i + 1}" for i in range(len(loan_transaction_create_row))])
        values = tuple(loan_transaction_create_row.values())

        stmt = f"INSERT INTO loans ({columns}) VALUES ({placeholders}) RETURNING *"
        row = await self.connection.fetchrow(stmt, *values)
        return LoanDatabaseMapper.from_db_row_to_loan_transaction(row)

    async def update_loan_by_id(self, loan_id: int, loan_update: Loan) -> Loan:
        loan_update_row = LoanDatabaseMapper.from_loan_to_db_row(loan_update)
        columns = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(loan_update_row.keys())])
        values = tuple(loan_update_row.values()) + (loan_id,)
        stmt = f"UPDATE banks SET {columns} WHERE id = ${len(values)} RETURNING *"

        row = await self.connection.fetchrow(stmt, *values)
        if row:
            return LoanDatabaseMapper.from_db_row_to_loan(row)
        raise NotFoundError(f"Loan with id = {loan_id} not found")
