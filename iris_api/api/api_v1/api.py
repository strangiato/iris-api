"""Router for api endpoints."""
from fastapi import APIRouter

from iris_api.api.api_v1.endpoints import iris

api_v1_router = APIRouter()
api_v1_router.include_router(iris.router, prefix="/iris", tags=["iris"])
