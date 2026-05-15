from __future__ import annotations

import pandas as pd

from utils.config import ClimateAnalyticsConfig


def calculate_heatwave_days(
    df: pd.DataFrame,
    threshold: float = ClimateAnalyticsConfig.HEATWAVE_TEMP_THRESHOLD,
) -> pd.DataFrame:
    """Count days with maximum temperature above the heatwave threshold."""
    return (
        df[df["temp_max"] > threshold]
        .groupby("city")
        .size()
        .reset_index(name="heatwave_days")
    )


def calculate_coldwave_days(
    df: pd.DataFrame,
    threshold: float = ClimateAnalyticsConfig.COLDWAVE_TEMP_THRESHOLD,
) -> pd.DataFrame:
    """Count days with minimum temperature below the coldwave threshold."""
    return (
        df[df["temp_min"] < threshold]
        .groupby("city")
        .size()
        .reset_index(name="coldwave_days")
    )


def detect_heatwave_sequences(
    df: pd.DataFrame,
    threshold: float = ClimateAnalyticsConfig.HEATWAVE_SEQUENCE_THRESHOLD,
    min_duration: int = ClimateAnalyticsConfig.HEATWAVE_MIN_DURATION_DAYS,
) -> pd.DataFrame:
    """Detect consecutive heatwave periods meeting the configured duration."""
    columns = [
        "city",
        "sequence_id",
        "start_date",
        "end_date",
        "duration_days",
        "max_temperature",
    ]
    heatwave_df = df[df["temp_max"] >= threshold].copy()

    if heatwave_df.empty:
        return pd.DataFrame(columns=columns)

    heatwave_df = heatwave_df.sort_values(["city", "date"])
    heatwave_df["date_diff"] = (
        heatwave_df.groupby("city")["date"].diff().dt.days
    )
    heatwave_df["new_sequence"] = (heatwave_df["date_diff"] != 1).astype(int)
    heatwave_df["sequence_id"] = (
        heatwave_df.groupby("city")["new_sequence"].cumsum()
    )

    sequences = (
        heatwave_df.groupby(["city", "sequence_id"])
        .agg({"date": ["min", "max", "count"], "temp_max": "max"})
    )
    sequences.columns = [
        "start_date",
        "end_date",
        "duration_days",
        "max_temperature",
    ]
    sequences = sequences.reset_index()
    sequences = sequences[sequences["duration_days"] >= min_duration]
    return sequences.sort_values("duration_days", ascending=False)


def calculate_heatwave_severity(
    sequences_df: pd.DataFrame,
    threshold: float = ClimateAnalyticsConfig.HEATWAVE_SEQUENCE_THRESHOLD,
) -> pd.DataFrame:
    """Calculate a severity index for each heatwave sequence."""
    severity_df = sequences_df.copy()

    if severity_df.empty:
        severity_df["severity_index"] = pd.Series(dtype=float)
        return severity_df

    severity_df["severity_index"] = (
        severity_df["duration_days"]
        * (severity_df["max_temperature"] - threshold)
    ).round(2)
    return severity_df.sort_values("severity_index", ascending=False)

