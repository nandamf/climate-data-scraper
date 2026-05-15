from __future__ import annotations

import os
from typing import Any

import requests


class ClimateApiClient:
    """Small reusable client for the existing FastAPI climate analytics API."""

    def __init__(self, base_url: str | None = None, timeout: int = 10) -> None:
        self.base_url = (base_url or os.getenv("CLIMATE_API_URL") or "http://127.0.0.1:8000").rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Fetch a JSON response from the API."""
        response = requests.get(
            f"{self.base_url}{path}",
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def collection(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Return the `data` list from collection-style API responses."""
        payload = self.get(path, params=params)
        return payload.get("data", [])

    def health(self) -> dict[str, Any]:
        return self.get("/health")

    def cities(self) -> list[str]:
        payload = self.get("/cities")
        return payload.get("cities", [])

    def city_summary(self, city: str) -> dict[str, Any]:
        payload = self.get(f"/cities/{city}")
        return payload.get("data", {})

    def risk_ranking(self, limit: int = 100) -> list[dict[str, Any]]:
        return self.get("/analytics/risk-ranking", params={"limit": limit}).get("data", [])

    def warming_trends(self, city: str | None = None) -> list[dict[str, Any]]:
        params = {"city": city} if city else None
        return self.collection("/analytics/warming-trends", params=params)

    def yearly_temperatures(self, city: str | None = None) -> list[dict[str, Any]]:
        params = {"city": city} if city else None
        return self.collection("/analytics/yearly-temperatures", params=params)

    def anomalies(self, city: str | None = None, limit: int = 1000) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if city:
            params["city"] = city
        return self.collection("/analytics/anomalies", params=params)

    def heatwaves(self, limit: int = 100) -> list[dict[str, Any]]:
        return self.collection("/analytics/heatwaves", params={"limit": limit})

    def heatwave_severity(self, limit: int = 500) -> list[dict[str, Any]]:
        return self.collection("/analytics/heatwave-severity", params={"limit": limit})

    def variability(self, limit: int = 100) -> list[dict[str, Any]]:
        return self.collection("/analytics/variability", params={"limit": limit})

    def extremes(self, limit: int = 100) -> list[dict[str, Any]]:
        return self.collection("/analytics/extreme-temperatures", params={"limit": limit})


api_client = ClimateApiClient()

