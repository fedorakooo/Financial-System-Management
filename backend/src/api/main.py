from fastapi import APIRouter

from src.api.routes.banks.banks import router as banks_router
from src.api.routes.users.registration import router as registration_router
from src.api.routes.auth.auth import router as auth_router
from src.api.routes.users.users import router as users_router
from src.api.routes.users.profile import router as profile_router
from src.api.routes.enterprises.enterprises import router as enterprises_router
from src.api.routes.accounts.accounts import router as accounts_router

router = APIRouter()

router.include_router(banks_router)
router.include_router(registration_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(profile_router)
router.include_router(enterprises_router)
router.include_router(accounts_router)
