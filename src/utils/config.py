from __future__ import annotations

from pathlib import Path


class PipelineConfig:
    """Filesystem and ingestion configuration for the climate pipeline."""

    INPUT_DATA_PATH = Path("data/input/cities.csv")
    OUTPUT_DATA_DIR = Path("data/output")
    ANALYTICS_DIR = Path("data/analytics")
    LOGS_DIR = Path("logs")
    PIPELINE_LOG_PATH = LOGS_DIR / "pipeline.log"

    HISTORICAL_DATA_FILENAME = "historical_climate_data.csv"
    WEATHER_API_START_DATE = "2015-01-01"
    WEATHER_API_END_DATE = "2025-12-31"
    REQUEST_TIMEOUT_SECONDS = 10


class ClimateAnalyticsConfig:
    """Tunable analytics thresholds and weights."""

    HEATWAVE_TEMP_THRESHOLD = 35.0
    COLDWAVE_TEMP_THRESHOLD = 0.0
    HEATWAVE_SEQUENCE_THRESHOLD = 35.0
    HEATWAVE_MIN_DURATION_DAYS = 5
    ANOMALY_Z_SCORE_THRESHOLD = 2.0

    RISK_SCORE_WEIGHTS = {
        "warming_rate_per_year": 30,
        "temperature_variability": 2,
        "heatwave_days": 0.05,
        "seasonal_amplitude": 1.5,
    }

    ANALYTICS_EXPORTS = {
        "warming_trends": "warming_trends.csv",
        "temperature_variability": "temperature_variability.csv",
        "heatwave_days": "heatwave_days.csv",
        "coldwave_days": "coldwave_days.csv",
        "seasonal_amplitude": "seasonal_amplitude.csv",
        "extreme_temperatures": "extreme_temperatures.csv",
        "climate_risk_scores": "climate_risk_scores.csv",
        "temperature_anomalies": "temperature_anomalies.csv",
        "heatwave_sequences": "heatwave_sequences.csv",
        "heatwave_severity": "heatwave_severity.csv",
    }

