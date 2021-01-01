from fastapi import APIRouter

from tejas.api.api_v1.endpoints import utils

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
