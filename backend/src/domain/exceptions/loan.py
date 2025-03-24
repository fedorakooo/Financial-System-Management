class LoanError(Exception):
    """Base exception for loan handlers."""
    pass


class LoanAccountNotPendingError(LoanError):
    def __init__(self, message: str = "The loan account is not in pending status."):
        self.message = message
        super().__init__(self.message)
