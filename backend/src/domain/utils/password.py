import bcrypt


class PasswordHandler:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes password using bcrypt."""

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode('utf-8')

    @staticmethod
    def validate_password(password: str, hashed_password: str) -> bool:
        """Checks if the password you entered matches the hash."""

        return bcrypt.checkpw(password.encode(), hashed_password.encode())
