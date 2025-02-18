from fastapi import FastAPI

from src.api.main import router
from src.infrastructure.repositories.bank import BankRepository
from src.infrastructure.repositories.user import UserRepository

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await UserRepository.create_table()
    await BankRepository.create_table()

app.include_router(router)