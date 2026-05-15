from __future__ import annotations

from typing import Any

import pandas as pd

from utils.constants import (
    CITY_COLUMN,
    CLIMATE_DATA_COLUMNS,
    REQUIRED_DAILY_API_FIELDS,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def validate_cities_dataframe(df: pd.DataFrame) -> bool:
    """Validate that the input file contains usable city data."""
    if df.empty:
        logger.error("Input cities file is empty.")
        return False

    if CITY_COLUMN not in df.columns:
        logger.error("Input CSV must contain a '%s' column.", CITY_COLUMN)
        return False

    if df[CITY_COLUMN].dropna().empty:
        logger.error("Input CSV does not contain any valid city names.")
        return False

    return True


def validate_coordinates(coords: dict[str, Any] | None) -> bool:
    """Validate geocoder coordinates before calling the weather API."""
    if not coords:
        return False

    latitude = coords.get("latitude")
    longitude = coords.get("longitude")

    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        logger.warning("Invalid coordinate values: %s", coords)
        return False

    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        logger.warning("Coordinates out of range: %s", coords)
        return False

    return True


def validate_climate_api_response(data: dict[str, Any] | None) -> bool:
    """Validate Open-Meteo response shape for daily climate fields."""
    if not data or "daily" not in data:
        return False

    daily = data["daily"]
    if not isinstance(daily, dict):
        return False

    missing_fields = [
        field for field in REQUIRED_DAILY_API_FIELDS if field not in daily
    ]
    if missing_fields:
        logger.warning("Climate API response missing fields: %s", missing_fields)
        return False

    lengths = [len(daily[field]) for field in REQUIRED_DAILY_API_FIELDS]
    if len(set(lengths)) != 1:
        logger.warning("Climate API response fields have inconsistent lengths.")
        return False

    return True


def validate_climate_dataframe(df: pd.DataFrame) -> bool:
    """Validate transformed climate observations before export and analytics."""
    if df.empty:
        logger.error("Climate dataframe is empty.")
        return False

    missing_columns = [
        column for column in CLIMATE_DATA_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        logger.error("Climate dataframe missing columns: %s", missing_columns)
        return False

    return True

