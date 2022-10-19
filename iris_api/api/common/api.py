"""Router for common route endpoints."""
from fastapi import APIRouter

from iris_api.api.common.endpoints import health, root

api_common_router = APIRouter()
api_common_router.include_router(root.router)
api_common_router.include_router(health.router, prefix="/health", tags=["health"])
