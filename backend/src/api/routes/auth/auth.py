from fastapi import APIRouter, Depends, Form, HTTPException, status

from src.dependencies.auth import AuthDependencies
from src.domain.exceptions.repository import NotFoundError
from src.domain.schemas.token import TokenInfo
from src.services.auth.auth import AuthService

router = APIRouter(tags=["AuthJWT"])


@router.post("/login", response_model=TokenInfo, responses={
    401: {"description": "Invalid phone number or password"},
    404: {"description": "User not found"},
    500: {"description": "Unexpected server error"}
})
async def login(
        username: str = Form(...),
        password: str = Form(...),
        auth_service: AuthService = Depends(AuthDependencies.get_auth_service)
):
    try:
        access_token = await auth_service.authenticate_user(username, password)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the authentication process."
        )

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )

    return TokenInfo(
        access_token=access_token,
        token_type="Bearer"
    )