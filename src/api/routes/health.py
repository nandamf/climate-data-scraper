"""Health check and status endpoints."""

from fastapi import APIRouter

from api.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns the current status of the climate analytics API.
    """
    return HealthResponse(status="healthy", version="1.0.0")
