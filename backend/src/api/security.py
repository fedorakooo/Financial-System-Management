from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from dependency_injector.wiring import Provide, inject

from src.api.exceptions.exception_factory import HttpExceptionFactory
from src.application.abstractions.auth.auth import AbstractAuthService
from src.application.dtos.user import UserAccessDTO
from src.infrastructure.dependencies.app import Application
from src.infrastructure.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError, TokenDecodeError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@inject
def get_current_active_auth_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AbstractAuthService = Depends(
            Provide[Application.services.auth_service]
        )
) -> UserAccessDTO:
    try:
        return auth_service.get_current_active_auth_user(token)
    except ExpiredTokenError as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except InvalidTokenError as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except TokenDecodeError as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except Exception as exc:
        raise HttpExceptionFactory.create_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="")
