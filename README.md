# Climate Data Scraper & Analytics API

A professional climate intelligence platform that ingests historical weather data, performs advanced analytics, and exposes insights through a modern FastAPI backend.

## Overview

This project combines a modular data pipeline with a climate analytics engine and a professional API layer to provide actionable climate intelligence:

- **Data Ingestion**: Fetches historical climate data from Open-Meteo API for configured cities
- **Analytics Engine**: Performs comprehensive climate analysis (trends, anomalies, heatwaves, risk scoring)
- **Data Pipeline**: Orchestrates ingestion → transformation → validation → analytics → export
- **API Layer**: Exposes climate intelligence through a RESTful API with professional documentation

## Architecture

### Project Structure

```
climate-data-scraper/
├── src/
│   ├── api/                    # FastAPI layer (new)
│   │   ├── app.py              # FastAPI application factory
│   │   ├── schemas.py          # Pydantic response models
│   │   ├── data_loader.py      # Analytics data loading utilities
│   │   └── routes/
│   │       ├── health.py       # Health check endpoints
│   │       ├── cities.py       # City metadata endpoints
│   │       └── analytics.py    # Climate analytics endpoints
│   ├── analytics/              # Analytics modules
│   │   ├── trends.py           # Warming trend analysis
│   │   ├── anomalies.py        # Temperature anomaly detection
│   │   ├── heatwaves.py        # Heatwave detection & severity
│   │   ├── risk.py             # Climate risk scoring
│   │   └── variability.py      # Temperature variability metrics
│   ├── ingestion/              # Data ingestion layer
│   │   ├── weather_api.py      # Open-Meteo API client
│   │   └── geocoder.py         # City geocoding
│   ├── pipeline/               # Pipeline orchestration
│   │   └── climate_pipeline.py # Main pipeline coordinator
│   ├── processing/             # Data processing
│   │   ├── transformations.py  # Data transformation logic
│   │   ├── validators.py       # Data validation
│   │   └── exporters.py        # CSV export utilities
│   ├── services/               # Service layer
│   │   └── analytics_service.py # Analytics orchestration
│   ├── utils/                  # Utilities
│   │   ├── config.py           # Configuration constants
│   │   ├── constants.py        # Data column definitions
│   │   └── logger.py           # Logging setup
│   └── main.py                 # Pipeline CLI entrypoint
├── data/
│   ├── input/                  # Input city list
│   │   └── cities.csv
│   ├── output/                 # Pipeline output
│   │   ├── climate_data.csv
│   │   └── historical_climate_data.csv
│   └── analytics/              # Analytics outputs
│       ├── climate_risk_scores.csv
│       ├── warming_trends.csv
│       ├── heatwave_days.csv
│       ├── temperature_anomalies.csv
│       ├── extreme_temperatures.csv
│       ├── heatwave_severity.csv
│       ├── seasonal_amplitude.csv
│       └── ... (10 total analytics datasets)
├── logs/                       # Application logs
├── requirements.txt            # Python dependencies
├── run_api.py                  # API server entrypoint
└── README.md                   # This file
```

### Data Flow

```
Cities CSV
    ↓
Geocoding (get coordinates)
    ↓
Weather API (fetch historical data)
    ↓
Data Transformation & Validation
    ↓
Analytics Engine
    ├── Warming Trends
    ├── Temperature Anomalies
    ├── Heatwave Detection
    ├── Climate Risk Scoring
    ├── Temperature Variability
    ├── Seasonal Patterns
    └── Extreme Temperature Records
    ↓
CSV Exports (data/analytics/)
    ↓
FastAPI Layer (reads from CSVs)
    ↓
REST API Endpoints
```

## Installation

### Requirements

- Python 3.9+
- Virtual environment (recommended)

### Setup Steps

1. **Clone/Navigate to the project**
   ```bash
   cd climate-data-scraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Data Pipeline

Generate analytics data from configured cities:

```bash
python src/main.py
```

This:
1. Loads city names from `data/input/cities.csv`
2. Fetches historical climate data (2015-2025)
3. Runs analytics suite
4. Exports results to `data/analytics/`

### Running the API Server

Start the climate analytics API:

```bash
python run_api.py
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Interactive Swagger UI: `http://localhost:8000/docs`
- ReDoc HTML documentation: `http://localhost:8000/redoc`

## API Reference

### Base URL
```
http://localhost:8000
```

### Health Check

```
GET /health
```

Check API status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Cities

#### List all cities

```
GET /cities
```

Get all cities with available analytics data.

**Response:**
```json
{
  "total_cities": 15,
  "cities": ["Cairo", "Delhi", "Dubai", "Lagos", "London", ...]
}
```

#### City summary

```
GET /cities/{city}
```

Get comprehensive climate summary for a specific city.

**Parameters:**
- `city` (string, path): City name (case-insensitive)

**Response:**
```json
{
  "data": {
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
    "anomalies_detected": 12
  }
}
```

### Analytics Endpoints

#### Risk Ranking

```
GET /analytics/risk-ranking
```

Get climate risk ranking for all cities (highest risk first).

**Query Parameters:**
- `limit` (int, optional): Results to return (default: 10, max: 100)

**Response:**
```json
{
  "total_cities": 15,
  "limit": 10,
  "data": [
    {
      "city": "Dubai",
      "risk_score": 87.5,
      "warming_rate": 0.045,
      "temperature_variability": 8.2,
      "heatwave_days": 180,
      "seasonal_amplitude": 18.5
    }
  ]
}
```

#### Warming Trends

```
GET /analytics/warming-trends
```

Get linear warming trend for cities.

**Query Parameters:**
- `limit` (int, optional): Results to return
- `city` (string, optional): Filter by city name

**Response:**
```json
{
  "total_records": 15,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "Tokyo",
      "linear_trend": 0.042,
      "r_squared": 0.78
    }
  ]
}
```

#### Temperature Anomalies

```
GET /analytics/anomalies
```

Get detected temperature anomalies (2σ deviation from normal).

**Query Parameters:**
- `limit` (int, optional): Results to return (max: 1000)
- `city` (string, optional): Filter by city name

**Response:**
```json
{
  "total_records": 456,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "London",
      "date": "2023-08-15",
      "temperature_anomaly": 2.8
    }
  ]
}
```

#### Heatwave Statistics

```
GET /analytics/heatwaves
```

Get heatwave days for all cities.

**Query Parameters:**
- `limit` (int, optional): Results to return
- `sort` (string, optional): Sort field (currently: `heatwave_days`)

**Response:**
```json
{
  "total_records": 15,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "Phoenix",
      "heatwave_days": 145
    }
  ]
}
```

#### Heatwave Severity

```
GET /analytics/heatwave-severity
```

Get heatwave severity analysis.

**Query Parameters:**
- `limit` (int, optional): Results to return

**Response:**
```json
{
  "total_records": 15,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "Cairo",
      "severity": 8.9,
      "average_temperature": 42.3
    }
  ]
}
```

#### Extreme Temperatures

```
GET /analytics/extreme-temperatures
```

Get extreme (max/min) temperature records.

**Query Parameters:**
- `limit` (int, optional): Results to return

**Response:**
```json
{
  "total_records": 15,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "Moscow",
      "max_temperature": 35.8,
      "min_temperature": -42.3
    }
  ]
}
```

#### Temperature Variability

```
GET /analytics/variability
```

Get temperature variability metrics (standard deviation).

**Query Parameters:**
- `limit` (int, optional): Results to return

**Response:**
```json
{
  "total_records": 15,
  "limit": null,
  "filtered_by_city": null,
  "data": [
    {
      "city": "Seattle",
      "variability": 6.2
    }
  ]
}
```

#### City-Specific Anomalies

```
GET /analytics/cities/{city}/anomalies
```

Get temperature anomalies for a specific city.

**Parameters:**
- `city` (string, path): City name (case-insensitive)

**Query Parameters:**
- `limit` (int, optional): Results to return

**Response:**
```json
{
  "total_records": 12,
  "limit": null,
  "filtered_by_city": "Tokyo",
  "data": [
    {
      "city": "Tokyo",
      "date": "2023-07-23",
      "temperature_anomaly": 3.2
    }
  ]
}
```

#### City-Specific Heatwaves

```
GET /analytics/cities/{city}/heatwaves
```

Get heatwave data for a specific city.

**Parameters:**
- `city` (string, path): City name (case-insensitive)

**Response:**
```json
{
  "total_records": 1,
  "limit": null,
  "filtered_by_city": "Phoenix",
  "data": [
    {
      "city": "Phoenix",
      "heatwave_days": 145
    }
  ]
}
```

## API Examples

### Example: Get top 5 highest-risk cities

```bash
curl "http://localhost:8000/analytics/risk-ranking?limit=5"
```

### Example: Get all temperature anomalies for Tokyo

```bash
curl "http://localhost:8000/analytics/cities/Tokyo/anomalies"
```

### Example: Get warming trends sorted by city

```bash
curl "http://localhost:8000/analytics/warming-trends?limit=20"
```

### Example: Get complete climate summary for a city

```bash
curl "http://localhost:8000/cities/London"
```

## Architecture & Design Principles

### Modular Design

- **Ingestion Layer**: Handles external data sources (APIs, geocoding)
- **Processing Layer**: Transforms and validates data independently
- **Analytics Layer**: Computes metrics without coupling to storage
- **Service Layer**: Orchestrates analytics pipeline
- **API Layer**: Exposes analytics cleanly without duplicating logic
- **Utils**: Centralized configuration, logging, constants

### API Design

- **RESTful**: Standard HTTP verbs and resource-based endpoints
- **Stateless**: Each request contains all needed information
- **Documented**: Automatic Swagger/ReDoc with descriptive docstrings
- **Scalable**: Routes are modular and can be easily extended
- **Type-Safe**: Pydantic models enforce schema validation
- **Error Handling**: Consistent error responses with meaningful messages

### Data Flow

1. **Pipeline** generates analytics CSVs
2. **Data Loader** reads from CSVs (no database yet)
3. **Routes** expose endpoints using data loader
4. **Schemas** validate and document responses
5. **App** orchestrates routes and middleware

## Performance Considerations

### Current Implementation

- Analytics data loaded from CSV files
- In-memory caching recommended for production (see Future Enhancements)
- Suitable for ~10-20 cities with daily data

### Future Enhancements

**Database Integration:**
```python
# In a future version, replace CSV loading with:
from sqlalchemy import create_engine

# Add database connection pooling
# Implement query optimization and indexing
# Add incremental data refresh
```

**Caching:**
```python
from fastapi_cache2 import FastAPICache2

# Cache analytics responses with TTL
# Invalidate on pipeline runs
# Implement cache warming
```

**Scalability:**
- Load analytics data once at startup
- Implement background refresh tasks
- Add pagination for large datasets
- Consider data compression

## Configuration

### Analytics Thresholds

Adjust thresholds in [src/utils/config.py](src/utils/config.py):

```python
class ClimateAnalyticsConfig:
    HEATWAVE_TEMP_THRESHOLD = 35.0        # Degrees Celsius
    COLDWAVE_TEMP_THRESHOLD = 0.0
    ANOMALY_Z_SCORE_THRESHOLD = 2.0       # Standard deviations
    HEATWAVE_MIN_DURATION_DAYS = 5
```

### Risk Score Weights

Customize risk calculation in [src/utils/config.py](src/utils/config.py):

```python
RISK_SCORE_WEIGHTS = {
    "warming_rate_per_year": 30,          # Warming trend importance
    "temperature_variability": 2,          # Climate unpredictability
    "heatwave_days": 0.05,                # Extreme heat frequency
    "seasonal_amplitude": 1.5,             # Seasonal extremes
}
```

### Input Cities

Add/modify cities in [data/input/cities.csv](data/input/cities.csv):

```csv
city
Tokyo
London
Dubai
New York
```

## Logging

Logs are written to [logs/pipeline.log](logs/pipeline.log)

View logs:
```bash
tail -f logs/pipeline.log
```

## Dependencies

See [requirements.txt](requirements.txt):

- **pandas**: Data processing
- **scikit-learn**: Statistical analysis
- **geopy**: Geocoding (city coordinates)
- **requests**: HTTP client
- **fastapi**: Web framework
- **uvicorn**: ASGI server

## Error Handling

### API Errors

| Status | Meaning | Example |
|--------|---------|---------|
| 200 | Success | City found, data returned |
| 400 | Bad Request | Invalid query parameters |
| 404 | Not Found | City not found, no analytics data |
| 500 | Server Error | Unexpected exception |
| 503 | Service Unavailable | Analytics data not generated yet |

### Common Issues

**"Analytics data not available yet"** (503)
- Run pipeline: `python src/main.py`
- Check `data/analytics/` directory

**"City not found"** (404)
- Check available cities: `GET /cities`
- Verify spelling and case

## Development

## Climate Intelligence Dashboard

The project now includes a professional Dash + Plotly dashboard that consumes
the existing FastAPI endpoints. The dashboard does not recompute analytics in
the frontend; it reads climate intelligence from the API and renders analytical
views for investigation.

### Dashboard Overview

The dashboard is designed as a desktop-first environmental analytics interface:

- **Overview**: climate risk ranking, warming leaders, heatwave severity, and instability tables
- **Warming Trends**: annual temperature evolution and warming-rate comparison
- **Anomalies**: anomaly timelines, z-score distribution, and extreme event records
- **Heatwaves**: heatwave frequency, event severity, duration distribution, and event explorer
- **City Analysis**: city-level climate profile with risk, anomalies, heatwaves, extremes, and variability

### Dashboard Architecture

```text
src/dashboard/
├── app.py                  # Dash application factory
├── layout.py               # Navigation shell and page container
├── api/
│   └── client.py           # Reusable FastAPI client
├── pages/
│   ├── overview.py
│   ├── warming_trends.py
│   ├── anomalies.py
│   ├── heatwaves.py
│   └── city_analysis.py
├── components/
│   ├── charts.py           # Plotly chart builders
│   ├── filters.py          # Reusable filter controls
│   └── tables.py           # Compact analytical tables
└── assets/
    └── styles.css          # Custom dashboard styling
```

### How To Run

First generate analytics data if needed:

```bash
python src/main.py
```

Start the FastAPI backend:

```bash
python run_api.py
```

In a second terminal, start the dashboard:

```bash
python run_dashboard.py
```

Open:

```text
http://localhost:8050
```

The dashboard expects the API at `http://127.0.0.1:8000` by default. To point it
at another API instance:

```bash
set CLIMATE_API_URL=http://127.0.0.1:8000
python run_dashboard.py
```

### API Integration

The dashboard consumes endpoints such as:

- `GET /cities`
- `GET /cities/{city}`
- `GET /analytics/risk-ranking`
- `GET /analytics/warming-trends`
- `GET /analytics/yearly-temperatures`
- `GET /analytics/anomalies`
- `GET /analytics/heatwaves`
- `GET /analytics/heatwave-severity`
- `GET /analytics/variability`
- `GET /analytics/extreme-temperatures`

### Registering Cities Through The API

The API can update the input city registry used by the ingestion pipeline.

Register a city without recalculating analytics:

```bash
curl -X POST "http://localhost:8000/cities" \
  -H "Content-Type: application/json" \
  -d "{\"city\":\"Phoenix, Arizona\"}"
```

Register a city and immediately refresh the pipeline:

```bash
curl -X POST "http://localhost:8000/cities?refresh=true" \
  -H "Content-Type: application/json" \
  -d "{\"city\":\"Dubai, United Arab Emirates\"}"
```

The `refresh=true` option runs ingestion and analytics, so it can take longer
because it calls geocoding and Open-Meteo. Without refresh, the city is only
added to `data/input/cities.csv`; run `python src/main.py` later to update the
analytics and dashboard.

### Screenshots

Add screenshots here after running the dashboard locally:

- Overview page
- Warming trends page
- Anomalies investigation page
- Heatwave intelligence page
- City climate profile

### Scalability Notes

- Add API response caching when the monitored city list grows.
- Move CSV-backed reads to a database for multi-user deployments.
- Add pagination parameters for high-volume anomaly/event endpoints.
- Expose more precomputed analytical endpoints instead of adding frontend calculations.
- Consider map-based geospatial views once city coordinates are exposed through the API.

### Running Tests

```bash
pytest tests/  # When tests are added
```

### Code Quality

```bash
# Formatting
black src/

# Linting
pylint src/

# Type checking
mypy src/
```

## Contributing

1. Maintain modular architecture
2. Add type hints to new code
3. Document public functions
4. Update this README for API changes
5. Test endpoints before committing


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

