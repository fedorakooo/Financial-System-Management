from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.dependencies.user import UserDependencies
from src.domain.exceptions.repository import NotFoundError, NoFieldsToUpdateError, UniqueConstraintError
from src.domain.schemas.user import UserRead, UserUpdate
from src.services.users.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserRead, responses={
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
async def get_user(
        user_id: int,
        user_service: UserService = Depends(UserDependencies.get_user_service)
) -> UserRead:
    try:
        user = await user_service.get_user_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred fetching the user."
        )
    return user


@router.get("/", response_model=List[UserRead], responses={
    500: {"description": "Unexpected server error"}
})
async def get_users(
        user_service: UserService = Depends(UserDependencies.get_user_service)
) -> List[UserRead]:
    try:
        users = await user_service.get_all_users()
    except Exception as e:
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
        user_service: UserService = Depends(UserDependencies.get_user_service)
) -> UserRead:
    try:
        updated_user = await user_service.update_user_by_id(user_id, user_update)
    except NotFoundError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )
    except NoFieldsToUpdateError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
            detail=f"An unexpected error occurred while updating the bank with id {user_id}."
        )
    return updated_user


@router.delete("/{user_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_user_by_id(
        user_id: int,
        user_service: UserService = Depends(UserDependencies.get_user_service)
):
    try:
        await user_service.delete_user_by_id(user_id)
    except NotFoundError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the user."
        )
    return {"message": "User deleted successfully"}
