from __future__ import annotations

import pandas as pd

from analytics.anomalies import detect_temperature_anomalies
from analytics.heatwaves import (
    calculate_coldwave_days,
    calculate_heatwave_days,
    calculate_heatwave_severity,
    detect_heatwave_sequences,
)
from analytics.risk import calculate_climate_risk_score
from analytics.trends import (
    calculate_linear_trend,
    calculate_warming_trend,
    calculate_yearly_average,
)
from analytics.variability import (
    calculate_extreme_temperatures,
    calculate_seasonal_amplitude,
    calculate_temperature_variability,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def run_climate_analytics(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run the complete climate analytics suite."""
    logger.info("Starting analytics execution.")

    yearly_avg = calculate_yearly_average(df)
    warming_delta = calculate_warming_trend(yearly_avg)
    linear_trend = calculate_linear_trend(yearly_avg)
    variability = calculate_temperature_variability(df)
    heatwave_days = calculate_heatwave_days(df)
    coldwave_days = calculate_coldwave_days(df)
    seasonal_amplitude = calculate_seasonal_amplitude(df)
    extreme_temperatures = calculate_extreme_temperatures(df)
    temperature_anomalies = detect_temperature_anomalies(df)
    heatwave_sequences = detect_heatwave_sequences(df)
    heatwave_severity = calculate_heatwave_severity(heatwave_sequences)
    climate_risk_scores = calculate_climate_risk_score(
        trend_df=linear_trend,
        variability_df=variability,
        heatwave_df=heatwave_days,
        amplitude_df=seasonal_amplitude,
    )

    logger.info("Analytics execution completed.")

    return {
        "yearly_average": yearly_avg,
        "warming_delta": warming_delta,
        "warming_trends": linear_trend,
        "temperature_variability": variability,
        "heatwave_days": heatwave_days,
        "coldwave_days": coldwave_days,
        "seasonal_amplitude": seasonal_amplitude,
        "extreme_temperatures": extreme_temperatures,
        "climate_risk_scores": climate_risk_scores,
        "temperature_anomalies": temperature_anomalies,
        "heatwave_sequences": heatwave_sequences,
        "heatwave_severity": heatwave_severity,
    }

