from __future__ import annotations

import pandas as pd

from utils.config import ClimateAnalyticsConfig


def detect_temperature_anomalies(
    df: pd.DataFrame,
    z_score_threshold: float = ClimateAnalyticsConfig.ANOMALY_Z_SCORE_THRESHOLD,
) -> pd.DataFrame:
    """Detect maximum-temperature anomalies relative to each city's baseline."""
    city_stats = df.groupby("city").agg({"temp_max": ["mean", "std"]})
    city_stats.columns = ["mean_temp", "std_temp"]
    city_stats = city_stats.reset_index()

    anomaly_df = df.merge(city_stats, on="city")
    anomaly_df["z_score"] = (
        anomaly_df["temp_max"] - anomaly_df["mean_temp"]
    ) / anomaly_df["std_temp"]
    anomaly_df["temperature_anomaly"] = (
        anomaly_df["temp_max"] - anomaly_df["mean_temp"]
    ).round(2)

    anomalies = anomaly_df[anomaly_df["z_score"].abs() > z_score_threshold]
    return anomalies[
        ["city", "date", "temp_max", "temperature_anomaly", "z_score"]
    ].sort_values("z_score", ascending=False)

