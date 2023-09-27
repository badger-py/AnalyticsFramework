from fastapi import APIRouter

from .click_details import router as click_details_router

v1_api_router = APIRouter()

v1_api_router.include_router(click_details_router, prefix="/clickdetails")
