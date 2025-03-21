from fastapi import FastAPI
from src.api.main import router

from src.api.startup import app_startup
from src.infrastructure.dependencies.setup import setup_container

container = setup_container()

app = FastAPI()

app.container = container

app.add_event_handler("startup", app_startup)

app.include_router(router)
