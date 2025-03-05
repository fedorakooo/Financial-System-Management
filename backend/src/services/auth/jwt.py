import jwt
from datetime import timedelta, datetime
from typing import Optional, Union

from src.config import settings
from src.domain.exceptions.jwt import InvalidTokenError, ExpiredTokenError, TokenDecodeError, TokenCreationError


class JWTService:
    def __init__(
            self,
            private_key: str = settings.auth_jwt.private_key_path.read_text(),
            public_key: str = settings.auth_jwt.public_key_path.read_text(),
            algorithm: str = settings.auth_jwt.algorithm,
            expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def encode(
            self,
            payload: dict,
            expire_timedelta: Optional[timedelta] = None
    ) -> str:
        """Generate JWT-token."""

        to_encode = payload.copy()
        now = datetime.utcnow()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=self.expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now
        )

        try:
            encoded = jwt.encode(
                to_encode,
                self.private_key,
                algorithm=self.algorithm
            )
        except Exception as e:
            raise TokenCreationError("Failed to create token")

        return encoded

    def decode(
            self,
            token: Union[str, bytes]
    ) -> dict:
        """Decodes JWT-token."""

        try:
            decoded = jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenError("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("The token is invalid.")
        except Exception as e:
            raise TokenDecodeError("Failed to decode token")

        return decoded
