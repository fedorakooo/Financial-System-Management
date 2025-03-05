from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.user import UserDependencies
from src.domain.exceptions.repository import UniqueConstraintError
from src.domain.schemas.user import UserRead, UserCreate
from src.services.users.user import UserService

router = APIRouter(prefix="/registration", tags=["Registration"])


@router.post("/", response_model=UserRead, responses={
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def user_registration(
        user: UserCreate,
        user_service: UserService = Depends(UserDependencies.get_user_service)
) -> UserRead:
    try:
        user = await user_service.create_user(user)
    except UniqueConstraintError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the bank."
        )
    return user
