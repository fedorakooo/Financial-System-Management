from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.auth import AuthDependencies
from src.dependencies.user import UserDependencies
from src.domain.exceptions.repository import NoFieldsToUpdateError, NotFoundError, UniqueConstraintError
from src.domain.schemas.user import UserRead, UserUpdate
from src.services.users.user import UserService

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=UserRead, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    500: {"description": "Unexpected server error"}
})
async def get_profile(
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user)
) -> UserRead:
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
        user_service: UserService = Depends(UserDependencies.get_user_service)
) -> UserRead:
    try:
        updated_user = await user_service.update_user_by_id(user.id, user_update)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except NoFieldsToUpdateError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )
    except UniqueConstraintError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the profile."
        )

    return updated_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, responses={
    401: {"description": "Invalid or expired token"},
    403: {"description": "User is inactive"},
    404: {"description": "User not found for deletion"},
    500: {"description": "Unexpected server error"}
})
async def delete_profile(
        user: UserRead = Depends(AuthDependencies.get_current_active_auth_user),
        user_service: UserService = Depends(UserDependencies.get_user_service)
):
    try:
        await user_service.delete_user_by_id(user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the user."
        )
