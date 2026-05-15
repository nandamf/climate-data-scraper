from __future__ import annotations

from typing import Any

import pandas as pd

from utils.constants import DATE_COLUMN, TEMP_MAX_COLUMN, TEMP_MIN_COLUMN


def climate_response_to_dataframe(
    city: str,
    coordinates: dict[str, Any],
    climate_data: dict[str, Any],
) -> pd.DataFrame:
    """Transform a validated Open-Meteo response into daily climate rows."""
    daily_data = climate_data["daily"]

    df = pd.DataFrame(
        {
            DATE_COLUMN: pd.to_datetime(daily_data["time"]),
            TEMP_MAX_COLUMN: daily_data["temperature_2m_max"],
            TEMP_MIN_COLUMN: daily_data["temperature_2m_min"],
        }
    )
    df["year"] = df[DATE_COLUMN].dt.year
    df["month"] = df[DATE_COLUMN].dt.month_name()
    df["city"] = city
    df["latitude"] = coordinates["latitude"]
    df["longitude"] = coordinates["longitude"]

    return df

