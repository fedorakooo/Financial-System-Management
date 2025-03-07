from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.dependencies.logs import LogDependencies
from src.dependencies.user import UserDependencies
from src.domain.exceptions.repository import NotFoundError, NoFieldsToUpdateError, UniqueConstraintError
from src.domain.schemas.user import UserRead, UserUpdate
from src.services.logs.log import LogService
from src.services.users.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserRead, responses={
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
async def get_user_by_id(
        user_id: int,
        user_service: UserService = Depends(UserDependencies.get_user_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> UserRead:
    try:
        user = await user_service.get_user_by_id(user_id)
        log_service.info(f"Successfully fetched user with ID {user_id}")
    except NotFoundError as e:
        log_service.warning(f"User with ID {user_id} not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"Unexpected error fetching user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred fetching the user."
        )
    return user


@router.get("/", response_model=List[UserRead], responses={
    500: {"description": "Unexpected server error"}
})
async def get_users(
        user_service: UserService = Depends(UserDependencies.get_user_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> List[UserRead]:
    try:
        users = await user_service.get_all_users()
        log_service.info(f"Successfully fetched {len(users)} users")
    except Exception as e:
        log_service.error(f"Unexpected error fetching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred fetching fetching the list of users."
        )
    return users


@router.patch("/{user_id}", response_model=UserRead, responses={
    404: {"description": "User not found"},
    400: {"description": "No fields to update"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def update_user_by_id(
        user_id: int,
        user_update: UserUpdate,
        user_service: UserService = Depends(UserDependencies.get_user_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> UserRead:
    log_service.info(f"Updating user with ID {user_id}")
    try:
        updated_user = await user_service.update_user_by_id(user_id, user_update)
        log_service.info(f"User with ID {user_id} successfully updated")
    except NotFoundError as e:
        log_service.error(f"User with ID {user_id} not found for update: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except NoFieldsToUpdateError as e:
        log_service.error(f"No fields to update for user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UniqueConstraintError as e:
        log_service.error(f"Unique constraint violation while updating user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"Unexpected error while updating user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the bank with id {user_id}."
        )
    return updated_user


@router.delete("/{user_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_user_by_id(
        user_id: int,
        user_service: UserService = Depends(UserDependencies.get_user_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
):
    log_service.info(f"Deleting user with ID {user_id}")
    try:
        await user_service.delete_user_by_id(user_id)
        log_service.info(f"User with ID {user_id} deleted successfully")
    except NotFoundError as e:
        log_service.warning(f"User with ID {user_id} not found for deletion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"Unexpected error while deleting user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the user."
        )
    return {"message": "User deleted successfully"}
