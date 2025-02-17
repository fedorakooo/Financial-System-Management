class RepositoryError(Exception):
    """Base exception for repository errors."""
    pass


class NotFoundError(RepositoryError):
    """Exception raised when a record is not found."""

    def __init__(self, item_id: int):
        super().__init__(f"Item with id {item_id} not found.")
        self.item_id = item_id


class UniqueConstraintError(RepositoryError):
    """Exception raised when a unique constraint is violated."""

    def __init__(self, field: str, value: str):
        super().__init__(f"Value '{value}' for field '{field}' violates unique constraint.")
        self.field = field
        self.value = value


class NoFieldsToUpdateError(RepositoryError):
    """Exception raised when there are no fields to update."""

    def __init__(self):
        super().__init__("No fields to update.")
