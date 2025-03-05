import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseModel):
    host: str = os.environ.get("DB_HOST")
    name: str = os.environ.get("DB_NAME")
    user: str = os.environ.get("DB_USER")
    password: str = os.environ.get("DB_PASS")

    url: str = f"postgres://{user}:{password}@{host}/{name}"
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseModel):
    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
