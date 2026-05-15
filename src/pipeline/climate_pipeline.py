from __future__ import annotations

import pandas as pd

from ingestion.geocoder import get_coordinates
from ingestion.weather_api import get_historical_climate
from processing.exporters import (
    ensure_directories,
    export_analytics_results,
    export_historical_data,
)
from processing.transformations import climate_response_to_dataframe
from processing.validators import (
    validate_cities_dataframe,
    validate_climate_dataframe,
    validate_coordinates,
)
from services.analytics_service import run_climate_analytics
from utils.config import PipelineConfig
from utils.constants import CITY_COLUMN
from utils.logger import get_logger

logger = get_logger(__name__)


class ClimatePipeline:
    """Coordinate climate ingestion, transformation, analytics, and exports."""

    def __init__(self, input_path=PipelineConfig.INPUT_DATA_PATH) -> None:
        self.input_path = input_path

    def run(self) -> bool:
        """Execute the end-to-end climate intelligence pipeline."""
        ensure_directories()

        cities = self.load_cities()
        if cities.empty:
            return False

        climate_df = self.collect_climate_data(cities)
        if not validate_climate_dataframe(climate_df):
            logger.error("Pipeline aborted due to invalid climate dataset.")
            return False

        export_historical_data(climate_df)

        analytics_results = run_climate_analytics(climate_df)
        export_analytics_results(analytics_results)

        logger.info("Climate pipeline completed successfully.")
        return True

    def load_cities(self) -> pd.Series:
        """Load city names from the configured input CSV."""
        try:
            cities_df = pd.read_csv(self.input_path)
        except FileNotFoundError:
            logger.error("Input file not found: %s", self.input_path)
            return pd.Series(dtype=str)

        if not validate_cities_dataframe(cities_df):
            return pd.Series(dtype=str)

        return cities_df[CITY_COLUMN].dropna().astype(str)

    def collect_climate_data(self, cities: pd.Series) -> pd.DataFrame:
        """Fetch and transform daily climate data for each configured city."""
        city_frames: list[pd.DataFrame] = []

        for city in cities:
            logger.info("Processing city: %s", city)
            coordinates = get_coordinates(city)

            if not validate_coordinates(coordinates):
                continue

            climate_data = get_historical_climate(
                latitude=coordinates["latitude"],
                longitude=coordinates["longitude"],
            )
            if not climate_data:
                logger.warning("No valid climate data for %s", city)
                continue

            try:
                city_df = climate_response_to_dataframe(
                    city=city,
                    coordinates=coordinates,
                    climate_data=climate_data,
                )
            except (KeyError, ValueError, TypeError) as exc:
                logger.error("Error transforming climate data for %s: %s", city, exc)
                continue

            city_frames.append(city_df)

        if not city_frames:
            logger.error("No data fetched for any city.")
            return pd.DataFrame()

        return pd.concat(city_frames, ignore_index=True)

