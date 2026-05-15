from __future__ import annotations

import pandas as pd


def calculate_temperature_variability(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate temperature variability as the average std dev of max/min temperatures."""
    variability = (
        df.groupby("city")
        .agg({"temp_max": "std", "temp_min": "std"})
        .round(2)
        .reset_index()
    )
    variability["temperature_variability"] = (
        variability["temp_max"] + variability["temp_min"]
    ) / 2
    return variability[["city", "temperature_variability"]]


def calculate_seasonal_amplitude(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate seasonal amplitude from monthly average maximum temperatures."""
    monthly_avg = (
        df.groupby(["city", "month"])
        .agg({"temp_max": "mean"})
        .reset_index()
    )

    amplitude = monthly_avg.groupby("city").agg({"temp_max": ["max", "min"]})
    amplitude.columns = ["max_temp", "min_temp"]
    amplitude = amplitude.reset_index()
    amplitude["seasonal_amplitude"] = (
        amplitude["max_temp"] - amplitude["min_temp"]
    ).round(2)

    return amplitude[["city", "seasonal_amplitude"]]


def calculate_extreme_temperatures(df: pd.DataFrame) -> pd.DataFrame:
    """Find the hottest and coldest recorded temperatures per city."""
    extremes = (
        df.groupby("city")
        .agg({"temp_max": "max", "temp_min": "min"})
        .reset_index()
    )
    extremes.columns = ["city", "hottest_day", "coldest_day"]
    return extremes

