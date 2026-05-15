# Climate Analytics API - Quick Start Guide

## Installation & Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Analytics Data
```bash
python src/main.py
```

This fetches climate data, runs analytics, and exports to `data/analytics/`

### 3. Start API Server
```bash
python run_api.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 4. Test the API

Visit in browser or use curl:

```bash
# Health check
curl http://localhost:8000/health

# List cities
curl http://localhost:8000/cities

# Get API documentation
# Visit: http://localhost:8000/docs
```

---

## 10 Essential Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```
Returns: `{"status": "healthy", "version": "1.0.0"}`

### 2. List All Cities
```bash
curl http://localhost:8000/cities
```
Returns: List of all available cities with count

### 3. City Summary
```bash
curl http://localhost:8000/cities/Tokyo
```
Returns: Comprehensive climate metrics for Tokyo

### 4. Risk Ranking (Top 5)
```bash
curl "http://localhost:8000/analytics/risk-ranking?limit=5"
```
Returns: Cities ranked by climate risk score

### 5. Warming Trends
```bash
curl http://localhost:8000/analytics/warming-trends
```
Returns: Temperature warming rate per city (°C/year)

### 6. Temperature Anomalies (Top 10)
```bash
curl "http://localhost:8000/analytics/anomalies?limit=10"
```
Returns: Extreme temperature events detected

### 7. Anomalies for Specific City
```bash
curl "http://localhost:8000/analytics/cities/London/anomalies?limit=5"
```
Returns: Temperature anomalies detected in London

### 8. Heatwave Statistics
```bash
curl http://localhost:8000/analytics/heatwaves
```
Returns: Number of heatwave days per city

### 9. City Heatwaves
```bash
curl http://localhost:8000/analytics/cities/Tokyo/heatwaves
```
Returns: Heatwave data for Tokyo

### 10. Extreme Temperatures
```bash
curl http://localhost:8000/analytics/extreme-temperatures
```
Returns: Maximum and minimum temperatures per city

---

## Interactive API Documentation

FastAPI automatically generates interactive documentation:

**Swagger UI** (Full interactive docs):
```
http://localhost:8000/docs
```

**ReDoc** (Clean HTML documentation):
```
http://localhost:8000/redoc
```

**OpenAPI Schema**:
```
http://localhost:8000/openapi.json
```

---

## Common Tasks

### Filter Results by City
```bash
curl "http://localhost:8000/analytics/anomalies?city=New%20York"
```

### Limit Results
```bash
curl "http://localhost:8000/analytics/risk-ranking?limit=3"
```

### Combine Filters
```bash
curl "http://localhost:8000/analytics/anomalies?city=Tokyo&limit=20"
```

### Test in Python
```python
import requests

response = requests.get("http://localhost:8000/cities")
print(response.json())

response = requests.get("http://localhost:8000/cities/Tokyo")
city_data = response.json()['data']
print(f"Risk Score: {city_data['risk_score']}")
```

---

## File Structure

```
climate-data-scraper/
├── src/
│   ├── api/                          ← NEW API LAYER
│   │   ├── __init__.py
│   │   ├── app.py                    ← FastAPI app
│   │   ├── schemas.py                ← Response models
│   │   ├── data_loader.py            ← CSV loader
│   │   └── routes/
│   │       ├── health.py
│   │       ├── cities.py
│   │       └── analytics.py
│   │
│   ├── analytics/                    ← Existing analytics
│   ├── ingestion/                    ← Existing ingestion
│   ├── pipeline/                     ← Existing pipeline
│   ├── processing/                   ← Existing processing
│   ├── services/                     ← Existing services
│   ├── utils/                        ← Existing utils
│   └── main.py                       ← Pipeline entrypoint
│
├── data/
│   ├── analytics/                    ← Analytics CSV output
│   ├── input/                        ← Input city list
│   └── output/                       ← Pipeline output
│
├── logs/
├── run_api.py                        ← API server start
├── requirements.txt                  ← Dependencies
├── README.md                         ← Main documentation
├── API_IMPLEMENTATION.md             ← Implementation guide
├── API_RESPONSES.md                  ← Example responses
├── test_data_loader.py              ← Data validation tests
└── [project files...]
```

---

## API Response Format

All analytics endpoints return:
```json
{
  "total_records": 15,
  "limit": 10,
  "filtered_by_city": null,
  "data": [
    {
      "city": "Tokyo",
      "metric": "value",
      ...
    }
  ]
}
```

---

## Troubleshooting

### "Analytics data not available yet" (503)
- Run the pipeline first: `python src/main.py`
- Check that CSV files exist in `data/analytics/`

### "City not found" (404)
- Check available cities: `curl http://localhost:8000/cities`
- Verify spelling and spacing

### "Connection refused"
- Ensure server is running: `python run_api.py`
- Check port 8000 is available

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Ensure you're in the project directory

---

## Performance Tips

1. **Run pipeline once**: Analytics data is cached in CSVs
2. **Keep server running**: API responds immediately to cached data
3. **Use pagination**: Add `?limit=100` to limit response size
4. **Filter by city**: Reduces JSON response size
5. **Cache responses**: Consider Redis for high-traffic deployments

---

## Stopping the Server

```bash
# Press Ctrl+C in the terminal running the API
```

Or kill the process:
```bash
# On Windows (PowerShell)
Get-Process python | Stop-Process

# On Linux/Mac
pkill -f "run_api.py"
```

---

## Next Steps

1. ✓ Start API: `python run_api.py`
2. ✓ Explore docs: `http://localhost:8000/docs`
3. ✓ Test endpoints using curl/Postman
4. ✓ Integrate with your frontend/application
5. ✓ Read full documentation in `README.md`
6. ✓ See implementation details in `API_IMPLEMENTATION.md`

---

## Example Integration (Python)

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Get risk ranking
response = requests.get(f"{BASE_URL}/analytics/risk-ranking?limit=5")
risks = response.json()
print(f"Top risk cities: {[r['city'] for r in risks['data']]}")

# Get Tokyo summary
response = requests.get(f"{BASE_URL}/cities/Tokyo")
tokyo = response.json()['data']
print(f"Tokyo risk: {tokyo['risk_score']}, Warming: {tokyo['warming_rate']}")

# Get anomalies
response = requests.get(f"{BASE_URL}/analytics/anomalies?city=London&limit=5")
anomalies = response.json()
for record in anomalies['data']:
    print(f"{record['date']}: {record['temperature_anomaly']:+.1f}°C")
```

---

## For More Information

- **Main README**: `README.md`
- **Implementation Details**: `API_IMPLEMENTATION.md`
- **Response Examples**: `API_RESPONSES.md`
- **Interactive Docs**: `http://localhost:8000/docs`

---

**Everything is ready! Start the API and begin exploring climate intelligence.** 🌍📊
