from typing import Any
from inflection import tableize


class RepositoryError(Exception):
    """Base exception for repository errors."""
    pass


class NotFoundError(RepositoryError):
    """Exception raised when a record is not found."""

    def __init__(self, entity: str, field: str, value: Any):
        self.entity = entity
        self.field = field
        self.value = value
        super().__init__(f"{entity} with {field} = {value} not found.")


class UniqueConstraintError(RepositoryError):
    """Exception raised when a unique constraint is violated."""

    def __init__(self, entity: str, field: str, value: str):
        self.entity = tableize(entity)
        self.field = field
        self.value = value
        super().__init__(f"Value '{value}' for field '{field}' in {entity} violates unique constraint.")


class NoFieldsToUpdateError(RepositoryError):
    """Exception raised when there are no fields to update."""

    DEFAULT_MESSAGE = "No fields to update."

    def __init__(self):
        super().__init__(self.DEFAULT_MESSAGE)


class ForeignKeyError(RepositoryError):
    """Exception raised when a foreign key constraint is violated."""

    def __init__(self, entity: str, field: str, value: Any, referenced_table: str):
        self.entity = entity
        self.field = field
        self.value = value
        self.referenced_table = referenced_table

        super().__init__(
            f"Foreign key violation: {entity}.{field} = {value} does not exist in {referenced_table}."
        )


class InsufficientFundsError(RepositoryError):
    """Exception raised when there are insufficient funds in the account."""

    def __init__(self, message="Insufficient funds", account_id: int = None):
        self.message = message
        self.account_id = account_id
        super().__init__(self.message)

    def __str__(self):
        return f"Account {self.account_id}: {self.message}" if self.account_id else self.message
