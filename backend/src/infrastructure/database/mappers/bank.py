from typing import Dict
from datetime import datetime
from src.domain.entities.bank import Bank


class BankDatabaseMapper:
    """Utility class for mapping between database rows and Bank entities."""

    @staticmethod
    def from_db_row(row: dict) -> Bank:
        return Bank(
            id=row["id"],
            name=row["name"],
            bic=row["bic"],
            address=row["address"],
            created_at=row["created_at"] if row["created_at"] else None,
            updated_at=row["updated_at"] if row["updated_at"] else datetime.now()
        )

    @staticmethod
    def to_db_row(bank: Bank) -> Dict:
        return {
            "name": bank.name,
            "bic": bank.bic,
            "address": bank.address,
            "created_at": bank.created_at,
            "updated_at": bank.updated_at
        }
