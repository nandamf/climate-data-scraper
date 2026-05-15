"""Analytics endpoints for climate intelligence data."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from api.data_loader import AnalyticsDataLoader
from api.schemas import (
    AnalyticsCollectionResponse,
    AnomalyRecord,
    ExtremeTemperaturesRecord,
    HeatwaveRecord,
    HeatwaveSeverityRecord,
    RiskRankingResponse,
    RiskScoreRecord,
    VariabilityRecord,
    WarmingTrendRecord,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/risk-ranking", response_model=RiskRankingResponse)
async def get_risk_ranking(limit: int = Query(10, ge=1, le=100)) -> RiskRankingResponse:
    """
    Get climate risk ranking for all cities.

    Cities are ranked by their climate risk score in descending order.
    Higher risk scores indicate greater climate vulnerability.

    Args:
        limit: Maximum number of results to return (default: 10, max: 100)

    Returns:
        Ranked list of cities by climate risk score
    """
    df = AnalyticsDataLoader.load_risk_scores()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    # Sort by risk score descending
    df = df.sort_values(by="climate_risk_score", ascending=False)
    total = len(df)

    # Apply limit
    df = df.head(limit)

    records = [
        RiskScoreRecord(
            city=row["city"],
            risk_score=float(row.get("climate_risk_score", 0)),
            warming_rate=float(row.get("warming_rate_per_year", 0)),
            temperature_variability=float(row.get("temperature_variability", 0)),
            heatwave_days=int(row.get("heatwave_days", 0)),
            seasonal_amplitude=float(row.get("seasonal_amplitude", 0)),
        )
        for _, row in df.iterrows()
    ]

    return RiskRankingResponse(
        total_cities=total,
        limit=limit,
        data=records,
    )


@router.get("/warming-trends", response_model=AnalyticsCollectionResponse)
async def get_warming_trends(
    limit: Optional[int] = Query(None, ge=1, le=100),
    city: Optional[str] = Query(None),
) -> AnalyticsCollectionResponse:
    """
    Get warming trend analysis for cities.

    Shows linear temperature trends (degrees per year) for each city.

    Args:
        limit: Maximum number of results (optional)
        city: Filter by city name (optional, case-insensitive)

    Returns:
        Warming trend records for cities
    """
    df = AnalyticsDataLoader.load_warming_trends()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    if city:
        df = df[df["city"].str.lower() == city.lower()]
        if df.empty:
            raise HTTPException(
                status_code=404, detail=f"No data found for city: {city}"
            )

    total = len(df)
    if limit:
        df = df.head(limit)

    records = [row.to_dict() for _, row in df.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=total,
        limit=limit,
        filtered_by_city=city,
        data=records,
    )


@router.get("/yearly-temperatures", response_model=AnalyticsCollectionResponse)
async def get_yearly_temperatures(
    city: Optional[str] = Query(None),
) -> AnalyticsCollectionResponse:
    """
    Get yearly average temperature evolution for trend visualization.

    The endpoint reads the historical climate export and returns annual
    averages so dashboards can render temporal views through the API.
    """
    df = AnalyticsDataLoader.load_yearly_temperatures()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Historical climate data not available yet"
        )

    if city:
        df = df[df["city"].str.lower() == city.lower()]
        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No yearly temperature data found for city: {city}",
            )

    records = [row.to_dict() for _, row in df.iterrows()]
    return AnalyticsCollectionResponse(
        total_records=len(records),
        limit=None,
        filtered_by_city=city,
        data=records,
    )


@router.get("/anomalies", response_model=AnalyticsCollectionResponse)
async def get_temperature_anomalies(
    limit: Optional[int] = Query(None, ge=1, le=1000),
    city: Optional[str] = Query(None),
) -> AnalyticsCollectionResponse:
    """
    Get detected temperature anomalies.

    Anomalies are temperatures that deviate significantly (>2σ) from historical norms.

    Args:
        limit: Maximum number of results (optional)
        city: Filter by city name (optional, case-insensitive)

    Returns:
        Temperature anomaly records with dates and magnitudes
    """
    df = AnalyticsDataLoader.load_anomalies()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    if city:
        df = df[df["city"].str.lower() == city.lower()]
        if df.empty:
            raise HTTPException(
                status_code=404, detail=f"No anomalies found for city: {city}"
            )

    # Sort by absolute anomaly magnitude descending
    df["abs_anomaly"] = df["temperature_anomaly"].abs()
    df = df.sort_values(by="abs_anomaly", ascending=False)

    total = len(df)
    if limit:
        df = df.head(limit)

    records = [row.drop("abs_anomaly").to_dict() for _, row in df.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=total,
        limit=limit,
        filtered_by_city=city,
        data=records,
    )


@router.get("/heatwaves", response_model=AnalyticsCollectionResponse)
async def get_heatwave_data(
    limit: Optional[int] = Query(None, ge=1, le=100),
    sort: str = Query("heatwave_days", pattern="^(heatwave_days)$"),
) -> AnalyticsCollectionResponse:
    """
    Get heatwave statistics for all cities.

    Shows the number of days each city experienced extreme heat conditions.

    Args:
        limit: Maximum number of results (optional)
        sort: Sort field (currently: heatwave_days)

    Returns:
        Heatwave day counts for all cities
    """
    df = AnalyticsDataLoader.load_heatwaves()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    # Sort descending
    df = df.sort_values(by=sort, ascending=False)
    total = len(df)

    if limit:
        df = df.head(limit)

    records = [row.to_dict() for _, row in df.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=total,
        limit=limit,
        filtered_by_city=None,
        data=records,
    )


@router.get("/heatwave-severity", response_model=AnalyticsCollectionResponse)
async def get_heatwave_severity(
    limit: Optional[int] = Query(None, ge=1, le=500),
) -> AnalyticsCollectionResponse:
    """
    Get heatwave event details with severity analysis.

    Shows individual heatwave events with duration, peak temperature, and severity index.

    Args:
        limit: Maximum number of results (optional)

    Returns:
        Individual heatwave events sorted by severity
    """
    df = AnalyticsDataLoader.load_heatwave_severity()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    df = df.sort_values(by="severity_index", ascending=False)
    total = len(df)

    if limit:
        df = df.head(limit)

    records = [row.to_dict() for _, row in df.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=total,
        limit=limit,
        filtered_by_city=None,
        data=records,
    )


@router.get("/extreme-temperatures", response_model=AnalyticsCollectionResponse)
async def get_extreme_temperatures(
    limit: Optional[int] = Query(None, ge=1, le=100),
) -> AnalyticsCollectionResponse:
    """
    Get extreme temperature records.

    Shows maximum and minimum temperatures recorded for each city.

    Args:
        limit: Maximum number of results (optional)

    Returns:
        Extreme temperature records for all cities
    """
    df = AnalyticsDataLoader.load_extreme_temperatures()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    total = len(df)
    if limit:
        df = df.head(limit)

    records = [row.to_dict() for _, row in df.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=total,
        limit=limit,
        filtered_by_city=None,
        data=records,
    )


@router.get("/variability", response_model=AnalyticsCollectionResponse)
async def get_temperature_variability(
    limit: Optional[int] = Query(None, ge=1, le=100),
) -> AnalyticsCollectionResponse:
    """
    Get temperature variability metrics.

    Variability measures how much temperature fluctuates (standard deviation).
    Higher values indicate more unpredictable climate patterns.

    Args:
        limit: Maximum number of results (optional)

    Returns:
        Temperature variability for all cities
    """
    df = AnalyticsDataLoader.load_variability()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    df = df.sort_values(by="temperature_variability", ascending=False)
    total = len(df)

    if limit:
        df = df.head(limit)

    records = [row.to_dict() for _, row in df.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=total,
        limit=limit,
        filtered_by_city=None,
        data=records,
    )


@router.get("/cities/{city}/anomalies", response_model=AnalyticsCollectionResponse)
async def get_city_anomalies(
    city: str,
    limit: Optional[int] = Query(None, ge=1, le=1000),
) -> AnalyticsCollectionResponse:
    """
    Get temperature anomalies for a specific city.

    Args:
        city: City name (case-insensitive)
        limit: Maximum number of results (optional)

    Returns:
        Temperature anomalies for the specified city

    Raises:
        404: If no data exists for the specified city
    """
    df = AnalyticsDataLoader.load_anomalies()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    df = df[df["city"].str.lower() == city.lower()]
    if df.empty:
        raise HTTPException(
            status_code=404, detail=f"No anomalies found for city: {city}"
        )

    df["abs_anomaly"] = df["temperature_anomaly"].abs()
    df = df.sort_values(by="abs_anomaly", ascending=False)

    total = len(df)
    if limit:
        df = df.head(limit)

    records = [row.drop("abs_anomaly").to_dict() for _, row in df.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=total,
        limit=limit,
        filtered_by_city=city,
        data=records,
    )


@router.get("/cities/{city}/heatwaves", response_model=AnalyticsCollectionResponse)
async def get_city_heatwaves(city: str) -> AnalyticsCollectionResponse:
    """
    Get heatwave data for a specific city.

    Args:
        city: City name (case-insensitive)

    Returns:
        Heatwave statistics for the specified city

    Raises:
        404: If no data exists for the specified city
    """
    df = AnalyticsDataLoader.load_heatwaves()
    if df.empty:
        raise HTTPException(
            status_code=503, detail="Analytics data not available yet"
        )

    city_data = df[df["city"].str.lower() == city.lower()]
    if city_data.empty:
        raise HTTPException(
            status_code=404, detail=f"No heatwave data found for city: {city}"
        )

    records = [row.to_dict() for _, row in city_data.iterrows()]

    return AnalyticsCollectionResponse(
        total_records=len(records),
        limit=None,
        filtered_by_city=city,
        data=records,
    )
