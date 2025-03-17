from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from dependency_injector.wiring import Provide, inject

from src.application.abstractions.auth.auth import AbstractAuthService
from src.infrastructure.dependencies.app import Application

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@inject
def get_current_active_auth_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AbstractAuthService = Depends(
            Provide[Application.services.auth_service]
        )
):
    return auth_service.get_current_active_auth_user(token)
