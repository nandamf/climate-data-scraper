"""Human-friendly labels for dashboard fields."""

FIELD_LABELS = {
    "city": "Cidade",
    "date": "Data",
    "year": "Ano",
    "avg_temperature": "Temperatura média anual (C)",
    "temp_max": "Temperatura máxima (C)",
    "temp_min": "Temperatura mínima (C)",
    "temperature_anomaly": "Diferença da temperatura normal (C)",
    "z_score": "Intensidade do desvio",
    "risk_score": "Risco climático",
    "climate_risk_score": "Risco climático",
    "warming_rate": "Aquecimento por ano (C)",
    "warming_rate_per_year": "Aquecimento por ano (C)",
    "temperature_variability": "Variação de temperatura",
    "heatwave_days": "Dias de calor extremo",
    "coldwave_days": "Dias de frio extremo",
    "seasonal_amplitude": "Diferença entre estações (C)",
    "hottest_day": "Maior temperatura (C)",
    "coldest_day": "Menor temperatura (C)",
    "start_date": "Início",
    "end_date": "Fim",
    "duration_days": "Duração (dias)",
    "max_temperature": "Pico de temperatura (C)",
    "severity_index": "Severidade da onda de calor",
    "sequence_id": "Evento",
}


def label_for(field: str) -> str:
    """Return a friendly label for a data field."""
    return FIELD_LABELS.get(field, field.replace("_", " ").title())


def labels_for(fields: list[str]) -> dict[str, str]:
    """Return Plotly labels for selected fields."""
    return {field: label_for(field) for field in fields}

