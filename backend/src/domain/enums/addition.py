from enum import Enum


class AdditionSource(Enum):
    BANK_TRANSFER = "BANK_TRANSFER"
    CARD_PAYMENT = "CARD_PAYMENT"
    CASH = "CASH"
    CRYPTO = "CRYPTO"
    OTHER = "OTHER"

class AdditionStatus(Enum):
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
