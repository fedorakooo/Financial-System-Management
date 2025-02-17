import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class DbSettings(BaseModel):
    host: str = os.environ.get("DB_HOST")
    name: str = os.environ.get("DB_NAME")
    user: str = os.environ.get("DB_USER")
    password: str = os.environ.get("DB_PASS")

    url: str = f"postgres://{user}:{password}@{host}/{name}"
    echo: bool = True


class Settings(BaseModel):
    db: DbSettings = DbSettings()


settings = Settings()
