"""Route for health checks."""
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def health():
    """Return basic response for health check."""
    return {"healthcheck": "Everything OK!"}
