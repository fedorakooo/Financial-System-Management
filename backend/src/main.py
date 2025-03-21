from fastapi import FastAPI
from src.api.main import router
from src.infrastructure.database.database_initializer import DatabaseInitializer

app = FastAPI()

app.add_event_handler("startup", DatabaseInitializer.create_all_tables)

app.include_router(router)
