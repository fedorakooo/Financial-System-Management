from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.dependencies.additions import AdditionsDependencies
from src.dependencies.auth import AuthDependencies
from src.dependencies.logs import LogDependencies
from src.domain.exceptions.repository import UniqueConstraintError, ForeignKeyError, NotFoundError
from src.domain.schemas.addition import AdditionRead, AdditionCreate
from src.domain.schemas.user import UserRead
from src.services.additions.addition import AdditionService
from src.services.logs.log import LogService

router = APIRouter(prefix="/additions", tags=["Additions"])


@router.get("/{addition_id}", response_model=AdditionRead, responses={
    409: {"description": "An addition with these details already exists"},
    500: {"description": "Unexpected server error"}
})
async def get_addition_by_id(
        addition_id: int,
        addition_service: AdditionService = Depends(AdditionsDependencies.get_addition_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> AdditionRead:
    try:
        addition = await addition_service.get_addition_by_id(addition_id)
        log_service.info(f"Successfully fetched addition with ID {addition_id}")
    except NotFoundError as e:
        log_service.warning(f"Addition with ID {addition_id} not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"An unexpected error occurred while fetching the addition with ID {addition_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the addition."
        )
    return addition


@router.get("/", response_model=List[AdditionRead], responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
async def get_account_additions(
        account_id: int,
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        additions_service: AdditionService = Depends(AdditionsDependencies.get_addition_service)
) -> List[AdditionRead]:
    try:
        additions = await additions_service.get_additions_by_account_id(account_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of additions."
        )
    return additions


@router.post("/", response_model=AdditionRead, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def create_addition(
        addition_create_request: AdditionCreate,
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        addition_service: AdditionService = Depends(AdditionsDependencies.get_addition_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> AdditionRead:
    log_service.info(f"Creating addition with Account ID {addition_create_request.account_id}")
    try:
        created_addition = await addition_service.create_addition(addition_create_request, user.id)
        log_service.info(
            f"Addition with Account ID {created_addition.account_id} and ID {created_addition.id} successfully created")
    except UniqueConstraintError as e:
        log_service.error(
            f"Unique constraint violation while creating the addition with Account ID {addition_create_request.account_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ForeignKeyError as e:
        log_service.error(
            f"Foreign key constraint violation while creating the addition with Account ID {addition_create_request.account_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(
            f"An unexpected error occurred while creating the addition with Account ID {addition_create_request.account_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the addition."
        )
    return created_addition
