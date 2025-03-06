from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.logs import LogDependencies
from src.dependencies.user import UserDependencies
from src.domain.exceptions.repository import UniqueConstraintError
from src.domain.schemas.user import UserRead, UserCreate
from src.services.logs.log import LogService
from src.services.users.user import UserService

router = APIRouter(prefix="/registration", tags=["Registration"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED, responses={
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def user_registration(
        user: UserCreate,
        user_service: UserService = Depends(UserDependencies.get_user_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> UserRead:
    log_service.info(f"Attempting to register a new user with phone_number: {user.phone_number}")
    try:
        created_user = await user_service.create_user(user)
        log_service.info(
            f"User successfully registered with phone_number {created_user.phone_number} and ID {created_user.id}"
        )
    except UniqueConstraintError as e:
        log_service.error(
            f"Unique constraint violation while creating user with phone_number {user.phone_number}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"Unexpected error occurred during user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while user registration."
        )
    return created_user
