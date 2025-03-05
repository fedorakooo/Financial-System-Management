from typing import Optional

from src.services.users.user import UserService
from src.services.auth.jwt import JWTService
from src.domain.utils.password import PasswordHandler


class AuthService:
    def __init__(self, user_service: UserService, jwt_service: JWTService):
        self.user_service = user_service
        self.jwt_service = jwt_service

    async def validate_auth_user(self, phone_number: str, password: str) -> bool:
        """Validate user credentials and return True if valid, else False."""

        hashed_password = await self.user_service.get_users_hashed_password_by_phone_number(phone_number)

        if not hashed_password or not PasswordHandler.validate_password(password, hashed_password):
            return False

        return True

    def create_access_token(self, phone_number: str) -> str:
        """Generate JWT token for the given phone number."""

        payload = {"sub": phone_number}
        access_token = self.jwt_service.encode(payload=payload)
        return access_token

    async def authenticate_user(self, phone_number: str, password: str) -> Optional[str]:
        """Validate user credentials and return access token if valid, else return None."""

        is_valid = await self.validate_auth_user(phone_number, password)
        if not is_valid:
            return None

        return self.create_access_token(phone_number)