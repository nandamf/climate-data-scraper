"""Utility functions for loading analytics data from CSV files."""

from __future__ import annotations

import pandas as pd
from pathlib import Path

from utils.config import PipelineConfig
from utils.logger import get_logger

logger = get_logger(__name__)


class AnalyticsDataLoader:
    """Load climate analytics data from CSV files."""

    @staticmethod
    def load_risk_scores() -> pd.DataFrame:
        """Load climate risk scores for all cities."""
        filepath = PipelineConfig.ANALYTICS_DIR / "climate_risk_scores.csv"
        if not filepath.exists():
            logger.warning("Risk scores file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_warming_trends() -> pd.DataFrame:
        """Load warming trend data for all cities."""
        filepath = PipelineConfig.ANALYTICS_DIR / "warming_trends.csv"
        if not filepath.exists():
            logger.warning("Warming trends file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_anomalies() -> pd.DataFrame:
        """Load temperature anomaly data."""
        filepath = PipelineConfig.ANALYTICS_DIR / "temperature_anomalies.csv"
        if not filepath.exists():
            logger.warning("Anomalies file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_heatwaves() -> pd.DataFrame:
        """Load heatwave day data for all cities."""
        filepath = PipelineConfig.ANALYTICS_DIR / "heatwave_days.csv"
        if not filepath.exists():
            logger.warning("Heatwaves file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_coldwaves() -> pd.DataFrame:
        """Load coldwave day data for all cities."""
        filepath = PipelineConfig.ANALYTICS_DIR / "coldwave_days.csv"
        if not filepath.exists():
            logger.warning("Coldwaves file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_heatwave_severity() -> pd.DataFrame:
        """Load heatwave severity data."""
        filepath = PipelineConfig.ANALYTICS_DIR / "heatwave_severity.csv"
        if not filepath.exists():
            logger.warning("Heatwave severity file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_extreme_temperatures() -> pd.DataFrame:
        """Load extreme temperature records."""
        filepath = PipelineConfig.ANALYTICS_DIR / "extreme_temperatures.csv"
        if not filepath.exists():
            logger.warning("Extreme temperatures file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_variability() -> pd.DataFrame:
        """Load temperature variability data."""
        filepath = PipelineConfig.ANALYTICS_DIR / "temperature_variability.csv"
        if not filepath.exists():
            logger.warning("Variability file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_seasonal_amplitude() -> pd.DataFrame:
        """Load seasonal amplitude data."""
        filepath = PipelineConfig.ANALYTICS_DIR / "seasonal_amplitude.csv"
        if not filepath.exists():
            logger.warning("Seasonal amplitude file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_historical_climate() -> pd.DataFrame:
        """Load historical daily climate observations."""
        filepath = (
            PipelineConfig.OUTPUT_DATA_DIR
            / PipelineConfig.HISTORICAL_DATA_FILENAME
        )
        if not filepath.exists():
            logger.warning("Historical climate file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def load_yearly_temperatures() -> pd.DataFrame:
        """Load yearly average temperatures from historical observations."""
        df = AnalyticsDataLoader.load_historical_climate()
        if df.empty:
            return pd.DataFrame()

        yearly = (
            df.groupby(["city", "year"])
            .agg({"temp_max": "mean", "temp_min": "mean"})
            .round(2)
            .reset_index()
        )
        yearly["avg_temperature"] = (
            yearly["temp_max"] + yearly["temp_min"]
        ) / 2
        return yearly

    @staticmethod
    def load_heatwave_sequences() -> pd.DataFrame:
        """Load heatwave sequence data."""
        filepath = PipelineConfig.ANALYTICS_DIR / "heatwave_sequences.csv"
        if not filepath.exists():
            logger.warning("Heatwave sequences file not found: %s", filepath)
            return pd.DataFrame()
        return pd.read_csv(filepath)

    @staticmethod
    def get_available_cities() -> list[str]:
        """Get list of available cities from risk scores."""
        df = AnalyticsDataLoader.load_risk_scores()
        if df.empty:
            return []
        return sorted(df["city"].unique().tolist())

    @staticmethod
    def get_city_data(
        city: str, df: pd.DataFrame
    ) -> dict | None:
        """Extract data for a specific city from a dataframe."""
        city_data = df[df["city"].str.lower() == city.lower()]
        if city_data.empty:
            return None
        return city_data.iloc[0].to_dict()

    @staticmethod
    def get_city_summary(city: str) -> dict | None:
        """Get comprehensive summary for a city across all analytics."""
        city_lower = city.lower()

        # Load all datasets
        risk_df = AnalyticsDataLoader.load_risk_scores()
        warmth_df = AnalyticsDataLoader.load_warming_trends()
        var_df = AnalyticsDataLoader.load_variability()
        heat_df = AnalyticsDataLoader.load_heatwaves()
        cold_df = AnalyticsDataLoader.load_coldwaves()
        seasonal_df = AnalyticsDataLoader.load_seasonal_amplitude()
        extreme_df = AnalyticsDataLoader.load_extreme_temperatures()
        severity_df = AnalyticsDataLoader.load_heatwave_severity()
        anom_df = AnalyticsDataLoader.load_anomalies()

        # Filter by city
        risk_data = risk_df[risk_df["city"].str.lower() == city_lower]
        if risk_data.empty:
            return None

        risk_row = risk_data.iloc[0]
        warmth_row = (
            warmth_df[warmth_df["city"].str.lower() == city_lower].iloc[0]
            if not warmth_df[warmth_df["city"].str.lower() == city_lower].empty
            else {}
        )
        var_row = (
            var_df[var_df["city"].str.lower() == city_lower].iloc[0]
            if not var_df[var_df["city"].str.lower() == city_lower].empty
            else {}
        )
        heat_row = (
            heat_df[heat_df["city"].str.lower() == city_lower].iloc[0]
            if not heat_df[heat_df["city"].str.lower() == city_lower].empty
            else {}
        )
        cold_row = (
            cold_df[cold_df["city"].str.lower() == city_lower].iloc[0]
            if not cold_df[cold_df["city"].str.lower() == city_lower].empty
            else {}
        )
        seasonal_row = (
            seasonal_df[seasonal_df["city"].str.lower() == city_lower].iloc[0]
            if not seasonal_df[seasonal_df["city"].str.lower() == city_lower].empty
            else {}
        )
        extreme_row = (
            extreme_df[extreme_df["city"].str.lower() == city_lower].iloc[0]
            if not extreme_df[extreme_df["city"].str.lower() == city_lower].empty
            else {}
        )
        severity_df_city = severity_df[severity_df["city"].str.lower() == city_lower]
        max_severity = (
            float(severity_df_city["severity_index"].max())
            if not severity_df_city.empty
            else 0.0
        )

        anomalies_count = len(anom_df[anom_df["city"].str.lower() == city_lower])

        return {
            "city": risk_row["city"],
            "risk_score": float(risk_row.get("climate_risk_score", 0)),
            "warming_rate": float(warmth_row.get("warming_rate_per_year", 0)),
            "temperature_variability": float(var_row.get("temperature_variability", 0)),
            "heatwave_days": int(heat_row.get("heatwave_days", 0)),
            "coldwave_days": int(cold_row.get("coldwave_days", 0)),
            "seasonal_amplitude": float(seasonal_row.get("seasonal_amplitude", 0)),
            "extreme_max": float(extreme_row.get("hottest_day", 0)),
            "extreme_min": float(extreme_row.get("coldest_day", 0)),
            "heatwave_severity": max_severity,
            "anomalies_detected": anomalies_count,
        }
