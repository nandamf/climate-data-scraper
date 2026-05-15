from __future__ import annotations

from typing import Optional, Union

from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

from utils.logger import get_logger

logger = get_logger(__name__)

geolocator = Nominatim(user_agent="climate_scraper")


def get_coordinates(city: str) -> Optional[dict[str, Union[str, float]]]:
    """Return latitude and longitude for a city name."""
    try:
        location = geolocator.geocode(city, timeout=10)
    except (GeocoderTimedOut, GeocoderServiceError) as exc:
        logger.error("Geocoding error for %s: %s", city, exc)
        return None

    if not location:
        logger.warning("Coordinates not found for city: %s", city)
        return None

    return {
        "city": city,
        "latitude": location.latitude,
        "longitude": location.longitude,
    }

