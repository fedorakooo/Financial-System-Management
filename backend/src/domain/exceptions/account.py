from decimal import Decimal

from src.domain.enums.account import AccountStatus


class AccountError(Exception):
    """Base exception for account handlers."""
    pass


class AccountAlreadyInRequestedStatusError(AccountError):
    """Exception raised when an account is already in the requested status."""

    def __init__(self, status: str):
        self.status = status
        super().__init__(f"Account is already in the requested status: {self.status}")


class StatusChangeNotAllowedError(AccountError):
    """Exception raised when a status change is not allowed."""

    def __init__(self, current_status: str, requested_status: str):
        self.current_status = current_status
        self.requested_status = requested_status
        super().__init__(
            f"Status change from {self.current_status} to {self.requested_status} is not allowed"
        )

class InsufficientFundsError(AccountError):
    """Exception raised when there are insufficient funds to perform an operation."""

    def __init__(self, current_balance: Decimal):
        self.current_balance = current_balance
        super().__init__(
            f"Insufficient funds. Current balance: {self.current_balance}"
        )

class InactiveAccountError(AccountError):
    """Exception raised when an operation is attempted on an inactive account."""

    def __init__(self, current_status: str):
        self.current_status = current_status
        super().__init__(
            f"Account must be {AccountStatus.ACTIVE} for this operation. Current status: {self.current_status}"
        )
