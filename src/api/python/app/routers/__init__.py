from fastapi import APIRouter

from .health_check import router as health_check_router
from .auth import router as auth_router
from .item import router as item_router
from .log import router as log_router

router = APIRouter()

router.include_router(health_check_router, prefix="/health_check", tags=["health_check"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])

router.include_router(item_router, prefix="/item", tags=["item"])
router.include_router(log_router, prefix="/log", tags=["log"])