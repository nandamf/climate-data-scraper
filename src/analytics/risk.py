from __future__ import annotations

import pandas as pd

from utils.config import ClimateAnalyticsConfig


def calculate_climate_risk_score(
    trend_df: pd.DataFrame,
    variability_df: pd.DataFrame,
    heatwave_df: pd.DataFrame,
    amplitude_df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate a composite climate risk score from core climate indicators."""
    weights = ClimateAnalyticsConfig.RISK_SCORE_WEIGHTS

    risk_df = trend_df.merge(variability_df, on="city", how="left")
    risk_df = risk_df.merge(heatwave_df, on="city", how="left")
    risk_df = risk_df.merge(amplitude_df, on="city", how="left")
    risk_df = risk_df.fillna(0)

    risk_df["climate_risk_score"] = (
        risk_df["warming_rate_per_year"] * weights["warming_rate_per_year"]
        + risk_df["temperature_variability"] * weights["temperature_variability"]
        + risk_df["heatwave_days"] * weights["heatwave_days"]
        + risk_df["seasonal_amplitude"] * weights["seasonal_amplitude"]
    ).round(2)

    return risk_df.sort_values("climate_risk_score", ascending=False)

