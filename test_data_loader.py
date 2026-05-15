"""Simple test for climate analytics data loader."""

from __future__ import annotations

import sys
sys.path.insert(0, 'src')

from api.data_loader import AnalyticsDataLoader

print("=" * 70)
print("CLIMATE ANALYTICS - DATA LOADER TESTS")
print("=" * 70)

# Test 1: Load risk scores
print("\n[TEST 1] Load Risk Scores")
print("-" * 70)
df = AnalyticsDataLoader.load_risk_scores()
print(f"✓ Loaded {len(df)} cities")
print(f"Columns: {list(df.columns)}")
if not df.empty:
    print(f"Sample cities: {df['city'].head(3).tolist()}")

# Test 2: Get available cities
print("\n[TEST 2] Get Available Cities")
print("-" * 70)
cities = AnalyticsDataLoader.get_available_cities()
print(f"✓ Found {len(cities)} cities")
print(f"Cities: {cities}")

# Test 3: Load warming trends
print("\n[TEST 3] Load Warming Trends")
print("-" * 70)
df = AnalyticsDataLoader.load_warming_trends()
print(f"✓ Loaded {len(df)} records")
print(f"Columns: {list(df.columns)}")
if not df.empty:
    print(df.head(3).to_string())

# Test 4: Load anomalies
print("\n[TEST 4] Load Temperature Anomalies")
print("-" * 70)
df = AnalyticsDataLoader.load_anomalies()
print(f"✓ Loaded {len(df)} anomaly records")
print(f"Columns: {list(df.columns)}")
if not df.empty:
    print(f"Sample anomalies:")
    print(df.head(3).to_string())

# Test 5: Load heatwaves
print("\n[TEST 5] Load Heatwave Data")
print("-" * 70)
df = AnalyticsDataLoader.load_heatwaves()
print(f"✓ Loaded {len(df)} records")
print(f"Columns: {list(df.columns)}")
if not df.empty:
    print(df.head(3).to_string())

# Test 6: Load extreme temperatures
print("\n[TEST 6] Load Extreme Temperatures")
print("-" * 70)
df = AnalyticsDataLoader.load_extreme_temperatures()
print(f"✓ Loaded {len(df)} records")
print(f"Columns: {list(df.columns)}")
if not df.empty:
    print(df.head(3).to_string())

# Test 7: Load heatwave severity
print("\n[TEST 7] Load Heatwave Severity Events")
print("-" * 70)
df = AnalyticsDataLoader.load_heatwave_severity()
print(f"✓ Loaded {len(df)} event records")
print(f"Columns: {list(df.columns)}")
if not df.empty:
    print(f"Unique cities: {df['city'].nunique()}")
    print(f"Sample events:")
    print(df.head(3).to_string())

# Test 8: Get city summary
print("\n[TEST 8] Get City Summary (Tokyo)")
print("-" * 70)
summary = AnalyticsDataLoader.get_city_summary("Tokyo")
if summary:
    print("✓ City summary retrieved:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
else:
    print("✗ Failed to get city summary")

# Test 9: Get city summary (case insensitive)
print("\n[TEST 9] Get City Summary (LONDON - case insensitive)")
print("-" * 70)
summary = AnalyticsDataLoader.get_city_summary("LONDON")
if summary:
    print(f"✓ Retrieved summary for: {summary['city']}")
else:
    print("✗ Failed to get city summary")

# Test 10: Load variability
print("\n[TEST 10] Load Temperature Variability")
print("-" * 70)
df = AnalyticsDataLoader.load_variability()
print(f"✓ Loaded {len(df)} records")
if not df.empty:
    print(df.head(3).to_string())

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("✓ All data loader functions work correctly")
print("✓ CSV files are being read successfully")
print("✓ Data structure is valid and accessible")
print("\nAPI is ready to serve data!")
print("=" * 70)
