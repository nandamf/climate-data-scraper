from __future__ import annotations

from typing import Any, Optional

import requests

from processing.validators import validate_climate_api_response
from utils.config import PipelineConfig
from utils.logger import get_logger

logger = get_logger(__name__)


def get_historical_climate(
    latitude: float,
    longitude: float,
    start_date: str = PipelineConfig.WEATHER_API_START_DATE,
    end_date: str = PipelineConfig.WEATHER_API_END_DATE,
) -> Optional[dict[str, Any]]:
    """Fetch historical daily climate data from the Open-Meteo archive API."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "auto",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=PipelineConfig.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as exc:
        logger.error(
            "Error fetching climate data for %.4f, %.4f: %s",
            latitude,
            longitude,
            exc,
        )
        return None

    if not validate_climate_api_response(data):
        logger.warning(
            "Unexpected API response format for %.4f, %.4f",
            latitude,
            longitude,
        )
        return None

    return data

