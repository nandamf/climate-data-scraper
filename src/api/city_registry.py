from __future__ import annotations

import pandas as pd

from utils.config import PipelineConfig
from utils.constants import CITY_COLUMN


class CityRegistry:
    """Manage the input city registry used by the ingestion pipeline."""

    @staticmethod
    def load_registered_cities() -> list[str]:
        """Return cities currently registered in the input CSV."""
        path = PipelineConfig.INPUT_DATA_PATH
        if not path.exists():
            return []

        df = pd.read_csv(path)
        if CITY_COLUMN not in df.columns:
            return []

        return (
            df[CITY_COLUMN]
            .dropna()
            .astype(str)
            .str.strip()
            .loc[lambda series: series != ""]
            .tolist()
        )

    @staticmethod
    def add_city(city: str) -> tuple[bool, list[str]]:
        """Add a city to the input registry.

        Returns:
            A tuple containing whether a new row was added and the full city list.
        """
        normalized_city = city.strip()
        cities = CityRegistry.load_registered_cities()

        existing = {registered.lower() for registered in cities}
        if normalized_city.lower() in existing:
            return False, cities

        cities.append(normalized_city)
        path = PipelineConfig.INPUT_DATA_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({CITY_COLUMN: cities}).to_csv(path, index=False)

        return True, cities

