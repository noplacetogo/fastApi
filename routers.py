from fastapi import APIRouter
from routes import api, upload, line, payment, email, sms

router = APIRouter()


router.include_router(
    api.router,
    prefix="/api"
)

router.include_router(
    upload.router,
    prefix="/upload"
)

router.include_router(
    line.router,
    prefix="/line"
)

router.include_router(
    email.router,
    prefix="/email"
)

router.include_router(
    sms.router,
    prefix="/sms"
)

router.include_router(
    payment.router,
    prefix="/payment"
)
