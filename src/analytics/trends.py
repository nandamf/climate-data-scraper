from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression


def calculate_yearly_average(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate average max, min, and mean temperatures per year and city."""
    yearly_avg = (
        df.groupby(["city", "year"])
        .agg({"temp_max": "mean", "temp_min": "mean"})
        .round(2)
        .reset_index()
    )
    yearly_avg["avg_temperature"] = (
        yearly_avg["temp_max"] + yearly_avg["temp_min"]
    ) / 2
    return yearly_avg


def calculate_warming_trend(yearly_avg: pd.DataFrame) -> pd.DataFrame:
    """Calculate warming between the first and last available year per city."""
    trend_data: list[dict[str, object]] = []

    for city in yearly_avg["city"].unique():
        city_df = yearly_avg[yearly_avg["city"] == city].sort_values("year")
        if city_df.empty:
            continue

        first_year = city_df.iloc[0]
        last_year = city_df.iloc[-1]
        warming = last_year["avg_temperature"] - first_year["avg_temperature"]

        trend_data.append(
            {
                "city": city,
                "warming_trend_10y": round(warming, 2),
            }
        )

    return pd.DataFrame(trend_data)


def calculate_linear_trend(yearly_avg: pd.DataFrame) -> pd.DataFrame:
    """Calculate the annual warming rate using linear regression."""
    trend_results: list[dict[str, object]] = []

    for city in yearly_avg["city"].unique():
        city_df = (
            yearly_avg[yearly_avg["city"] == city]
            .sort_values("year")
            .dropna(subset=["avg_temperature"])
        )

        if len(city_df) < 2:
            continue

        x = city_df["year"].values.reshape(-1, 1)
        y = city_df["avg_temperature"].values

        model = LinearRegression()
        model.fit(x, y)

        trend_results.append(
            {
                "city": city,
                "warming_rate_per_year": round(model.coef_[0], 3),
            }
        )

    return pd.DataFrame(trend_results)

