from enum import Enum


class EnumUtils:
    """Utilities for working with enums."""

    @staticmethod
    def convert_enums_to_values(data: dict) -> dict:
        """Converts the Enum values into their primitive representations."""
        return {k: v.value if isinstance(v, Enum) else v for k, v in data.items()}
