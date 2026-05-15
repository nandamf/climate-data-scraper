# Climate Analytics API - Response Examples

This document shows example JSON responses from each API endpoint.

---

## Health Check

### Request
```bash
GET /health
```

### Response (200 OK)
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Cities

### List All Cities

#### Request
```bash
GET /cities
```

#### Response (200 OK)
```json
{
  "total_cities": 5,
  "cities": ["London", "New York", "Paris", "San Diego", "Tokyo"]
}
```

### Get City Summary

#### Request
```bash
GET /cities/Tokyo
```

#### Response (200 OK)
```json
{
  "data": {
    "city": "Tokyo",
    "risk_score": 55.69,
    "warming_rate": 0.169,
    "temperature_variability": 8.34,
    "heatwave_days": 27,
    "coldwave_days": 305,
    "seasonal_amplitude": 21.72,
    "extreme_max": 38.2,
    "extreme_min": -7.3,
    "heatwave_severity": 0.0,
    "anomalies_detected": 30
  }
}
```

#### Response (404 Not Found)
```json
{
  "error": "City not found: InvalidCity",
  "available_cities": ["London", "New York", "Paris", "San Diego", "Tokyo"],
  "status_code": 404
}
```

---

## Analytics

### Climate Risk Ranking

#### Request
```bash
GET /analytics/risk-ranking?limit=3
```

#### Response (200 OK)
```json
{
  "total_cities": 5,
  "limit": 3,
  "data": [
    {
      "city": "New York",
      "risk_score": 61.62,
      "warming_rate": 0.086,
      "temperature_variability": 9.715,
      "heatwave_days": 24,
      "seasonal_amplitude": 25.61
    },
    {
      "city": "Tokyo",
      "risk_score": 55.69,
      "warming_rate": 0.169,
      "temperature_variability": 8.345,
      "heatwave_days": 27,
      "seasonal_amplitude": 21.72
    },
    {
      "city": "Paris",
      "risk_score": 44.12,
      "warming_rate": 0.081,
      "temperature_variability": 6.65,
      "heatwave_days": 22,
      "seasonal_amplitude": 18.19
    }
  ]
}
```

### Warming Trends

#### Request
```bash
GET /analytics/warming-trends
```

#### Response (200 OK)
```json
{
  "total_records": 5,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "London",
      "warming_rate_per_year": 0.123
    },
    {
      "city": "New York",
      "warming_rate_per_year": 0.086
    },
    {
      "city": "Paris",
      "warming_rate_per_year": 0.081
    },
    {
      "city": "San Diego",
      "warming_rate_per_year": 0.042
    },
    {
      "city": "Tokyo",
      "warming_rate_per_year": 0.169
    }
  ]
}
```

### Temperature Anomalies

#### Request
```bash
GET /analytics/anomalies?limit=2
```

#### Response (200 OK)
```json
{
  "total_records": 483,
  "limit": 2,
  "filtered_by_city": null,
  "data": [
    {
      "city": "London",
      "date": "2022-07-19",
      "temp_max": 37.9,
      "temperature_anomaly": 22.77,
      "z_score": 3.654770
    },
    {
      "city": "San Diego",
      "date": "2020-09-30",
      "temp_max": 36.5,
      "temperature_anomaly": 15.29,
      "z_score": 3.818982
    }
  ]
}
```

### Anomalies with City Filter

#### Request
```bash
GET /analytics/anomalies?city=Tokyo&limit=2
```

#### Response (200 OK)
```json
{
  "total_records": 30,
  "limit": 2,
  "filtered_by_city": "Tokyo",
  "data": [
    {
      "city": "Tokyo",
      "date": "2023-08-15",
      "temp_max": 39.2,
      "temperature_anomaly": 18.5,
      "z_score": 2.85
    },
    {
      "city": "Tokyo",
      "date": "2023-09-03",
      "temp_max": 38.1,
      "temperature_anomaly": 17.3,
      "z_score": 2.65
    }
  ]
}
```

### Heatwave Statistics

#### Request
```bash
GET /analytics/heatwaves?limit=3
```

#### Response (200 OK)
```json
{
  "total_records": 5,
  "limit": 3,
  "filtered_by_city": null,
  "data": [
    {
      "city": "New York",
      "heatwave_days": 24
    },
    {
      "city": "Paris",
      "heatwave_days": 22
    },
    {
      "city": "Tokyo",
      "heatwave_days": 27
    }
  ]
}
```

### Heatwave Severity Events

#### Request
```bash
GET /analytics/heatwave-severity?limit=2
```

#### Response (200 OK)
```json
{
  "total_records": 0,
  "limit": 2,
  "filtered_by_city": null,
  "data": []
}
```

*Note: Heatwave severity events are available when they are present in the analytics data.*

### Extreme Temperatures

#### Request
```bash
GET /analytics/extreme-temperatures
```

#### Response (200 OK)
```json
{
  "total_records": 5,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "London",
      "hottest_day": 37.9,
      "coldest_day": -10.3
    },
    {
      "city": "New York",
      "hottest_day": 40.4,
      "coldest_day": -20.5
    },
    {
      "city": "Paris",
      "hottest_day": 40.7,
      "coldest_day": -8.6
    },
    {
      "city": "San Diego",
      "hottest_day": 38.2,
      "coldest_day": -7.3
    },
    {
      "city": "Tokyo",
      "hottest_day": 38.2,
      "coldest_day": -7.3
    }
  ]
}
```

### Temperature Variability

#### Request
```bash
GET /analytics/variability
```

#### Response (200 OK)
```json
{
  "total_records": 5,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "London",
      "temperature_variability": 5.725
    },
    {
      "city": "New York",
      "temperature_variability": 9.715
    },
    {
      "city": "Paris",
      "temperature_variability": 6.65
    },
    {
      "city": "San Diego",
      "temperature_variability": 5.625
    },
    {
      "city": "Tokyo",
      "temperature_variability": 8.345
    }
  ]
}
```

### City-Specific Anomalies

#### Request
```bash
GET /analytics/cities/London/anomalies?limit=2
```

#### Response (200 OK)
```json
{
  "total_records": 95,
  "limit": 2,
  "filtered_by_city": "London",
  "data": [
    {
      "city": "London",
      "date": "2022-07-19",
      "temp_max": 37.9,
      "temperature_anomaly": 22.77,
      "z_score": 3.654770
    },
    {
      "city": "London",
      "date": "2023-06-21",
      "temp_max": 36.5,
      "temperature_anomaly": 21.05,
      "z_score": 3.42
    }
  ]
}
```

#### Response (404 Not Found)
```json
{
  "detail": "No anomalies found for city: InvalidCity"
}
```

### City-Specific Heatwaves

#### Request
```bash
GET /analytics/cities/Tokyo/heatwaves
```

#### Response (200 OK)
```json
{
  "total_records": 1,
  "limit": null,
  "filtered_by_city": "Tokyo",
  "data": [
    {
      "city": "Tokyo",
      "heatwave_days": 27
    }
  ]
}
```

#### Response (404 Not Found)
```json
{
  "detail": "No heatwave data found for city: InvalidCity"
}
```

---

## Error Responses

### 404 Not Found
```json
{
  "error": "Not found",
  "detail": "Path '/invalid/path' not found",
  "status_code": 404
}
```

### 503 Service Unavailable
```json
{
  "detail": "Analytics data not available yet"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "detail": "An unexpected error occurred",
  "status_code": 500
}
```

---

## Testing Responses

You can test these endpoints using curl:

```bash
# Test health
curl http://localhost:8000/health

# List cities
curl http://localhost:8000/cities

# Get risk ranking
curl "http://localhost:8000/analytics/risk-ranking?limit=5"

# Get city summary
curl http://localhost:8000/cities/Tokyo

# Get anomalies for a city
curl "http://localhost:8000/analytics/cities/Tokyo/anomalies?limit=5"

# Filter anomalies by city
curl "http://localhost:8000/analytics/anomalies?city=London"
```

---

## Response Formats

### Standard Analytics Collection Response
```json
{
  "total_records": <number>,
  "limit": <number or null>,
  "filtered_by_city": <string or null>,
  "data": [<array of records>]
}
```

### Pagination Example
```
?limit=10      # Return first 10 records
?limit=100     # Return first 100 records (max for most endpoints)
?limit=1000    # Return first 1000 records (for anomalies only)
```

### Filtering Example
```
?city=Tokyo                   # Case-insensitive filter by city
?city=New%20York&limit=10     # Combined filter and pagination
```

---

## Data Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `city` | string | City name |
| `risk_score` | float | Climate risk score (0-100) |
| `warming_rate` | float | Warming rate (°C/year) |
| `warming_rate_per_year` | float | Same as warming_rate |
| `temperature_variability` | float | Temperature std deviation |
| `heatwave_days` | int | Number of heatwave days |
| `coldwave_days` | int | Number of coldwave days |
| `seasonal_amplitude` | float | Seasonal temperature range |
| `hottest_day` | float | Maximum temperature (°C) |
| `coldest_day` | float | Minimum temperature (°C) |
| `temperature_anomaly` | float | Temperature deviation (°C) |
| `z_score` | float | Statistical z-score |
| `date` | string | Date in YYYY-MM-DD format |
| `severity_index` | float | Heatwave severity score |
| `duration_days` | int | Event duration in days |
