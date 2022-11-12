from fastapi import APIRouter
from routes import api, upload

router = APIRouter()


router.include_router(
    api.router,
    prefix="/api"
)

router.include_router(
    upload.router,
    prefix="/upload"
)
