from src.domain.utils.enums import EnumUtils

class FieldUtils:
    """Utilities for working with fields."""

    @staticmethod
    def get_updated_fields(update_data: dict) -> dict:
        """Filters fields with non-zero values and converts them using EnumUtils."""

        updated_fields = {key: value for key, value in update_data.items() if value is not None}
        return EnumUtils.convert_enums_to_values(updated_fields)
