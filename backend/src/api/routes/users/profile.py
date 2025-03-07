from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.auth import AuthDependencies
from src.dependencies.logs import LogDependencies
from src.dependencies.user import UserDependencies
from src.domain.abstractions.logger.logger import AbstractLogger
from src.domain.exceptions.repository import NoFieldsToUpdateError, NotFoundError, UniqueConstraintError
from src.domain.schemas.user import UserRead, UserUpdate
from src.services.logs.log import LogService
from src.services.users.user import UserService

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=UserRead, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
async def get_profile(
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        log_service: AbstractLogger = Depends(LogDependencies.get_log_service)
) -> UserRead:
    log_service.info(f"Successfully fetched profile for user_id = {user.id}")
    return user


@router.patch("/", response_model=UserRead, responses={
    400: {"description": "No fields to update"},
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def update_profile(
        user_update: UserUpdate,
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        user_service: UserService = Depends(UserDependencies.get_user_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> UserRead:
    log_service.info(f"User {user.id} is updating profile")
    try:
        updated_user = await user_service.update_user_by_id(user.id, user_update)
        log_service.info(f"Profile updated successfully for user_id = {updated_user.id}")
    except NotFoundError as e:
        log_service.error(f"User with ID {user.id} not found for update: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except NoFieldsToUpdateError as e:
        log_service.error(f"No fields to update for user with ID {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UniqueConstraintError as e:
        log_service.error(f"Unique constraint violation for user with ID {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"Unexpected error occurred while updating profile for user {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating profile."
        )
    return updated_user


@router.delete("/", response_model=dict, status_code=status.HTTP_200_OK, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    404: {"description": "User not found for deletion"},
    500: {"description": "Unexpected server error"}
})
async def delete_profile(
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        user_service: UserService = Depends(UserDependencies.get_user_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
):
    log_service.info(f"Attempting to delete profile for user_id = {user.id}")
    try:
        await user_service.delete_user_by_id(user.id)
        log_service.info(f"User with user_id = {user.id} deleted successfully.")
    except NotFoundError as e:
        log_service.error(f"User with ID {user.id} not found for deletion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"Unexpected error occurred while deleting profile for user {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the user."
        )
    return {"message": "Profile deleted successfully"}
