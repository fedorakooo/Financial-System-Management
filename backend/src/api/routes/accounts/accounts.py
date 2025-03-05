from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.dependencies.accounts import AccountDependencies
from src.dependencies.auth import AuthDependencies
from src.domain.exceptions.forbidden import ForbiddenError
from src.domain.exceptions.repository import UniqueConstraintError, NotFoundError, ForeignKeyError
from src.domain.schemas.account import AccountRead, AccountCreateRequest
from src.domain.schemas.user import UserRead
from src.services.accounts.account import AccountService

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", response_model=List[AccountRead], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
async def get_user_accounts(
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        account_service: AccountService = Depends(AccountDependencies.get_account_service)
) -> List[AccountRead]:
    try:
        accounts = await account_service.get_accounts_by_user_id(user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of accounts."
        )
    return accounts


@router.post("/", response_model=AccountRead, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def create_account(
        account_create: AccountCreateRequest,
        user: UserRead = Depends(AuthDependencies.get_current_auth_user),
        account_service: AccountService = Depends(AccountDependencies.get_account_service)
) -> AccountRead:
    try:
        created_account = await account_service.create_account(account_create, user.id)
    except UniqueConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ForeignKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the account."
        )
    return created_account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive or does not have permission"},
    404: {"description": "Account not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_account_by_id(
        account_id: int,
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        account_service: AccountService = Depends(AccountDependencies.get_account_service)
) -> None:
    try:
        await account_service.delete_account_by_id(account_id, user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ForbiddenError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the bank with id {account_id}."
        )
    return {"message": "Bank deleted successfully"}
