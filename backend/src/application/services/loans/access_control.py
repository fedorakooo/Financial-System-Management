from typing import Optional

from src.application.dtos.user import UserAccessDTO
from src.domain.enums.user import UserRole
from src.domain.exceptions.forbidden import ForbiddenError


class AdditionProfileAccessControlService:
    """Service for controlling access to loan profile operations."""

    @staticmethod
    def can_get_loans(loan_account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if loan_account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_loan_request(requesting_user: UserAccessDTO) -> bool:
        if UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()

    @staticmethod
    def can_create_loan_transaction(loan_account_owner_id: int, requesting_user: UserAccessDTO) -> bool:
        if loan_account_owner_id == requesting_user.id and UserRole(requesting_user.role) in [UserRole.CLIENT]:
            return True
        raise ForbiddenError()
