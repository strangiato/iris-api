"""Route for health checks."""
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def root():
    """Return basic hello world response on index."""
    return {"msg": "Welcome to the API."}
