"""Pydantic schemas for climate analytics API responses."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """API health status response."""

    status: str = Field(description="Service health status")
    version: str = Field(description="API version")


class CityMetrics(BaseModel):
    """Metrics for a single city."""

    city: str = Field(description="City name")
    data: dict[str, Any] = Field(description="City-specific metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Tokyo",
                "data": {
                    "warming_trend": 0.042,
                    "temperature_variability": 12.5,
                    "heatwave_days": 45,
                },
            }
        }


class CityCreateRequest(BaseModel):
    """Request body for registering a new city."""

    city: str = Field(
        min_length=2,
        description="City name or qualified place name, e.g. 'Phoenix, Arizona'",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Phoenix, Arizona",
            }
        }


class CityCreateResponse(BaseModel):
    """Response after registering a city."""

    city: str = Field(description="Submitted city name")
    created: bool = Field(description="Whether the city was added to the registry")
    refresh_requested: bool = Field(description="Whether analytics refresh was requested")
    refresh_completed: bool = Field(description="Whether the refresh completed successfully")
    registered_cities: list[str] = Field(description="All cities currently in the input registry")
    message: str = Field(description="Operational status message")


class RiskScoreRecord(BaseModel):
    """Climate risk score for a city."""

    city: str = Field(description="City name")
    risk_score: float = Field(description="Overall climate risk score (0-100)")
    warming_rate: float = Field(
        description="Warming rate per year (degrees Celsius)"
    )
    temperature_variability: float = Field(
        description="Temperature variability standard deviation"
    )
    heatwave_days: int = Field(description="Number of heatwave days")
    seasonal_amplitude: float = Field(description="Seasonal temperature amplitude")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Dubai",
                "risk_score": 87.5,
                "warming_rate": 0.045,
                "temperature_variability": 8.2,
                "heatwave_days": 180,
                "seasonal_amplitude": 18.5,
            }
        }


class WarmingTrendRecord(BaseModel):
    """Warming trend data for a city."""

    city: str = Field(description="City name")
    warming_rate_per_year: float = Field(description="Warming rate (°C/year)")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Tokyo",
                "warming_rate_per_year": 0.042,
            }
        }


class AnomalyRecord(BaseModel):
    """Temperature anomaly detection for a city."""

    city: str = Field(description="City name")
    date: str = Field(description="Date (YYYY-MM-DD format)")
    temperature_anomaly: float = Field(description="Temperature anomaly (°C)")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "London",
                "date": "2023-08-15",
                "temperature_anomaly": 2.8,
            }
        }


class HeatwaveRecord(BaseModel):
    """Heatwave detection for a city."""

    city: str = Field(description="City name")
    heatwave_days: int = Field(description="Number of heatwave days")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Phoenix",
                "heatwave_days": 145,
            }
        }


class HeatwaveSeverityRecord(BaseModel):
    """Heatwave event details with severity metrics."""

    city: str = Field(description="City name")
    sequence_id: int = Field(description="Heatwave event identifier")
    start_date: str = Field(description="Event start date (YYYY-MM-DD)")
    end_date: str = Field(description="Event end date (YYYY-MM-DD)")
    duration_days: int = Field(description="Duration in days")
    max_temperature: float = Field(description="Peak temperature during event (°C)")
    severity_index: float = Field(description="Severity index score")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Cairo",
                "sequence_id": 1,
                "start_date": "2023-06-15",
                "end_date": "2023-06-22",
                "duration_days": 8,
                "max_temperature": 48.5,
                "severity_index": 8.9,
            }
        }


class ExtremeTemperaturesRecord(BaseModel):
    """Extreme temperature records for a city."""

    city: str = Field(description="City name")
    hottest_day: float = Field(description="Maximum temperature (°C)")
    coldest_day: float = Field(description="Minimum temperature (°C)")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Moscow",
                "hottest_day": 35.8,
                "coldest_day": -42.3,
            }
        }


class VariabilityRecord(BaseModel):
    """Temperature variability metrics for a city."""

    city: str = Field(description="City name")
    variability: float = Field(description="Temperature variability (standard deviation)")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Seattle",
                "variability": 6.2,
            }
        }


class RiskRankingResponse(BaseModel):
    """Risk ranking response with sorted records."""

    total_cities: int = Field(description="Total number of cities analyzed")
    limit: int = Field(description="Number of results returned")
    data: list[RiskScoreRecord] = Field(description="Risk scores ranked by severity")

    class Config:
        json_schema_extra = {
            "example": {
                "total_cities": 15,
                "limit": 10,
                "data": [
                    {
                        "city": "Dubai",
                        "risk_score": 87.5,
                        "warming_rate": 0.045,
                        "temperature_variability": 8.2,
                        "heatwave_days": 180,
                        "seasonal_amplitude": 18.5,
                    }
                ],
            }
        }


class AnalyticsCollectionResponse(BaseModel):
    """Generic response for analytics collections."""

    total_records: int = Field(description="Total number of records")
    limit: int | None = Field(
        description="Limit applied to results (None if no limit)"
    )
    filtered_by_city: str | None = Field(description="City filter applied (if any)")
    data: list[dict[str, Any]] = Field(description="Analytics records")

    class Config:
        json_schema_extra = {
            "example": {
                "total_records": 12,
                "limit": None,
                "filtered_by_city": None,
                "data": [
                    {
                        "city": "Tokyo",
                        "linear_trend": 0.042,
                        "r_squared": 0.78,
                    }
                ],
            }
        }


class CitySummaryResponse(BaseModel):
    """Comprehensive summary for a single city."""

    city: str = Field(description="City name")
    risk_score: float = Field(description="Climate risk score")
    warming_rate: float = Field(description="Warming rate (°C/year)")
    temperature_variability: float = Field(description="Temperature variability")
    heatwave_days: int = Field(description="Number of heatwave days")
    coldwave_days: int = Field(description="Number of coldwave days")
    seasonal_amplitude: float = Field(description="Seasonal amplitude")
    extreme_max: float = Field(description="Extreme maximum temperature (°C)")
    extreme_min: float = Field(description="Extreme minimum temperature (°C)")
    heatwave_severity: float = Field(description="Heatwave severity score")
    anomalies_detected: int = Field(description="Number of temperature anomalies")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Tokyo",
                "risk_score": 62.3,
                "warming_rate": 0.042,
                "temperature_variability": 12.5,
                "heatwave_days": 45,
                "coldwave_days": 28,
                "seasonal_amplitude": 24.8,
                "extreme_max": 40.7,
                "extreme_min": -10.2,
                "heatwave_severity": 6.5,
                "anomalies_detected": 12,
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(description="Error message")
    detail: str | None = Field(description="Additional error details")
    status_code: int = Field(description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "City not found",
                "detail": "No analytics data available for 'Atlantis'",
                "status_code": 404,
            }
        }
