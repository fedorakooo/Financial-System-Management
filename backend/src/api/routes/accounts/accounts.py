from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.dependencies.accounts import AccountDependencies
from src.dependencies.auth import AuthDependencies
from src.dependencies.logs import LogDependencies
from src.domain.exceptions.forbidden import ForbiddenError
from src.domain.exceptions.repository import UniqueConstraintError, NotFoundError, ForeignKeyError
from src.domain.schemas.account import AccountRead, AccountCreateRequest
from src.domain.schemas.user import UserRead
from src.services.accounts.account import AccountService
from src.services.logs.log import LogService

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", response_model=List[AccountRead], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
async def get_user_accounts(
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        account_service: AccountService = Depends(AccountDependencies.get_account_service),
        log_service: LogService = Depends(LogDependencies.get_log_service),
) -> List[AccountRead]:
    try:
        accounts = await account_service.get_accounts_by_user_id(user.id)
        log_service.info(f"Successfully fetched accounts for user ID {user.id}")
    except Exception as e:
        log_service.error(f"An unexpected error occurred while fetching accounts for user ID {user.id}: {str(e)}")
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
        account_service: AccountService = Depends(AccountDependencies.get_account_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> AccountRead:
    log_service.info(f"Creating account with Bank ID {account_create.bank_id}")
    try:
        created_account = await account_service.create_account(account_create, user.id)
        log_service.info(
            f"Account with Bank ID {created_account.bank_id} and ID {created_account.id} successfully created")
    except UniqueConstraintError as e:
        log_service.error(
            f"Unique constraint violation while creating the account with Bank ID {account_create.bank_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ForeignKeyError as e:
        log_service.error(
            f"Foreign key constraint violation while creating the account with Bank ID {account_create.bank_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(
            f"An unexpected error occurred while creating the account with Bank ID {account_create.bank_id}: {str(e)}"
        )
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
        account_service: AccountService = Depends(AccountDependencies.get_account_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> None:
    log_service.info(f"Deleting account with ID {account_id}")
    try:
        await account_service.delete_account_by_id(account_id, user.id)
        log_service.info(f"Account with ID {account_id} deleted successfully")
    except NotFoundError as e:
        log_service.warning(f"Account with ID {account_id} not found for deletion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ForbiddenError as e:
        log_service.error(f"Forbidden error while deleting the account with ID {account_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"An unexpected error while deleting the account with ID {account_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the account with id {account_id}."
        )
    return {"message": "Bank deleted successfully"}
