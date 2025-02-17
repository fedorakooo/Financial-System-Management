from fastapi import APIRouter

from src.api.routes.banks.banks import router as banks_router

router = APIRouter()

router.include_router(banks_router)
