"""City information and metadata endpoints."""

from fastapi import APIRouter, HTTPException, Query

from api.city_registry import CityRegistry
from api.data_loader import AnalyticsDataLoader
from api.schemas import CityCreateRequest, CityCreateResponse
from pipeline.climate_pipeline import ClimatePipeline

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("")
async def list_cities() -> dict:
    """
    List all available cities in the analytics database.

    Returns a sorted list of cities that have climate analytics data.
    """
    cities = AnalyticsDataLoader.get_available_cities()
    return {
        "total_cities": len(cities),
        "cities": cities,
    }


@router.get("/registered")
async def list_registered_cities() -> dict:
    """List cities registered for ingestion in data/input/cities.csv."""
    cities = CityRegistry.load_registered_cities()
    return {
        "total_cities": len(cities),
        "cities": cities,
    }


@router.post("", response_model=CityCreateResponse, status_code=201)
async def register_city(
    request: CityCreateRequest,
    refresh: bool = Query(
        False,
        description="Run the ingestion and analytics pipeline after adding the city.",
    ),
) -> CityCreateResponse:
    """Register a new city for future climate ingestion.

    By default this only updates data/input/cities.csv. Pass refresh=true to
    run the pipeline immediately and make the city available in analytics.
    """
    city = request.city.strip()
    if not city:
        raise HTTPException(status_code=400, detail="City name cannot be empty.")

    created, registered_cities = CityRegistry.add_city(city)
    refresh_completed = False

    if refresh:
        refresh_completed = ClimatePipeline().run()
        if not refresh_completed:
            raise HTTPException(
                status_code=500,
                detail="City was registered, but analytics refresh failed.",
            )

    if created and refresh_completed:
        message = "City registered and analytics refreshed."
    elif created:
        message = "City registered. Run the pipeline to update analytics."
    elif refresh_completed:
        message = "City already registered. Analytics refreshed."
    else:
        message = "City already registered."

    return CityCreateResponse(
        city=city,
        created=created,
        refresh_requested=refresh,
        refresh_completed=refresh_completed,
        registered_cities=registered_cities,
        message=message,
    )


@router.get("/{city}")
async def get_city_summary(city: str) -> dict:
    """
    Get comprehensive climate summary for a specific city.

    Includes risk score, warming trends, heatwaves, anomalies, and extremes.

    Args:
        city: City name (case-insensitive)

    Returns:
        Comprehensive climate metrics for the city

    Raises:
        404: If no data exists for the specified city
    """
    summary = AnalyticsDataLoader.get_city_summary(city)
    if summary is None:
        return {
            "error": f"City not found: {city}",
            "available_cities": AnalyticsDataLoader.get_available_cities(),
            "status_code": 404,
        }
    return {"data": summary}
