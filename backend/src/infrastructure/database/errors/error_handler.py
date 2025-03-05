from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from pydantic import BaseModel
from src.domain.exceptions.repository import UniqueConstraintError, ForeignKeyError


class ErrorHandler:
    """Class for handling database errors."""

    @staticmethod
    def handle_unique_violation(
            entity: str,
            error: UniqueViolationError,
            item: BaseModel
    ) -> UniqueConstraintError:
        """Handles unique constraint violation errors."""

        error_message = str(error).lower()
        for column in item.dict().keys():
            if column in error_message:
                return UniqueConstraintError(entity, column, item.dict()[column])

        return UniqueConstraintError(entity, "unknown_column", "unknown_value")

    @staticmethod
    def handle_foreign_key_violation(
            entity: str,
            error: ForeignKeyViolationError
    ) -> ForeignKeyError:
        """Handles foreign key constraint violation errors."""

        import re
        match = re.search(r"Key \((.*?)\)=\((.*?)\) is not present", error.detail)
        if match:
            field, value = match.group(1), match.group(2)
        else:
            field, value = "unknown_field", "unknown_value"

        referenced_table = error.constraint_name.split("_")[0] if error.constraint_name else "unknown_table"
        return ForeignKeyError(entity, field, value, referenced_table)

