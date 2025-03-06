from typing import Optional

from fastapi import Depends, HTTPException, status

from src.api.security import oauth2_scheme
from src.dependencies.logs import LogDependencies
from src.dependencies.user import UserDependencies
from src.domain.exceptions.repository import NotFoundError
from src.domain.schemas.user import UserRead
from src.services.auth.auth import AuthService
from src.services.auth.jwt import JWTService
from src.services.logs.log import LogService
from src.services.users.user import UserService
from src.domain.exceptions.jwt import ExpiredTokenError, InvalidTokenError, TokenDecodeError


class JWTDependencies:
    @staticmethod
    def get_jwt_service() -> JWTService:
        return JWTService()

    @staticmethod
    async def get_current_token_payload(
            token: str = Depends(oauth2_scheme),
            jwt_service: JWTService = Depends(get_jwt_service),
            log_service: LogService = Depends(LogDependencies.get_log_service)
    ) -> dict:
        try:
            payload = jwt_service.decode(token=token)

        except ExpiredTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except TokenDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            log_service.error(f"Unexpected error during token processing: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

        return payload


class AuthDependencies:
    @staticmethod
    def get_auth_service(
            user_service: UserService = Depends(UserDependencies.get_user_service),
            jwt_service: JWTService = Depends(JWTDependencies.get_jwt_service),
    ) -> AuthService:
        return AuthService(user_service, jwt_service)

    @staticmethod
    async def get_current_auth_user(
            payload: dict = Depends(JWTDependencies.get_current_token_payload),
            user_service: UserService = Depends(UserDependencies.get_user_service),
    ) -> UserRead:
        phone_number: Optional[str] = payload.get("sub")

        if not phone_number:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid: missing subject"
            )

        try:
            user = await user_service.get_user_by_phone_number(phone_number)
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid: user not found"
            )

        return user

    @staticmethod
    async def get_current_active_auth_user(
            user: UserRead = Depends(get_current_auth_user),
    ) -> UserRead:
        user = await user

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )

        return user
