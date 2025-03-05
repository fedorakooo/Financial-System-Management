class ForbiddenError(Exception):
    """Exception raised when a user tries to access a resource they don't have permission for."""

    def __init__(self):
        super().__init__("You do not have permission to perform this action.")
