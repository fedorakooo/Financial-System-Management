from enum import Enum


class AccountStatus(Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'
    FROZEN = 'FROZEN'
    ON_CONSIDERATION = 'ON_CONSIDERATION'
    CANCELLED = 'CANCELLED'
