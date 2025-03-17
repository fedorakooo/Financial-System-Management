from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.main import router
from src.api.startup import app_startup
from src.infrastructure.dependencies.setup import setup_container

container = setup_container()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.container = container

app.add_event_handler("startup", app_startup)

app.include_router(router)
