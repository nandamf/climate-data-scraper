from __future__ import annotations

from dash import Input, Output, callback, dcc, html

from dashboard.api.client import api_client
from dashboard.components.charts import line_chart, scatter_timeline
from dashboard.components.filters import city_dropdown
from dashboard.components.tables import analytical_table
from dashboard.pages.common import page_header, safe_api_call, section


def layout() -> html.Div:
    cities = safe_api_call(api_client.cities, [])
    default_city = cities[0] if cities else None
    summary = safe_api_call(lambda: api_client.city_summary(default_city), {}) if default_city else {}
    anomalies = safe_api_call(lambda: api_client.anomalies(city=default_city, limit=200), []) if default_city else []
    yearly = safe_api_call(lambda: api_client.yearly_temperatures(city=default_city), []) if default_city else []

    return html.Div(
        [
            page_header(
                "Perfil Climático da Cidade",
                "Resumo de risco, aquecimento, eventos fora do normal, calor extremo e recordes de temperatura.",
            ),
            html.Div(
                [city_dropdown(cities, "city-profile-selector", multi=False)],
                className="filter-row",
            ),
            html.Div(id="city-profile-summary", children=_summary_grid(summary)),
            html.Div(
                [
                    section(
                        "Temperatura média por ano",
                        dcc.Graph(
                            id="city-yearly-chart",
                            figure=line_chart(
                                yearly,
                                x="year",
                                y="avg_temperature",
                                color="city",
                                title="Evolução da temperatura média anual",
                            ),
                        ),
                    ),
                    section(
                        "Eventos fora do normal",
                        dcc.Graph(
                            id="city-anomaly-chart",
                            figure=scatter_timeline(
                                anomalies,
                                x="date",
                                y="temperature_anomaly",
                                color="city",
                                size="z_score",
                                title="Dias muito acima ou abaixo do padrão histórico",
                            ),
                        ),
                    ),
                ],
                className="grid two-col",
            ),
            section(
                "Eventos de temperatura da cidade",
                html.Div(
                    id="city-anomaly-table",
                    children=analytical_table(
                        anomalies,
                        "city-anomaly-records",
                        ["date", "temp_max", "temperature_anomaly", "z_score"],
                        page_size=10,
                    ),
                ),
            ),
        ],
        className="page",
    )


def _summary_grid(summary: dict) -> html.Div:
    fields = [
        ("Risco climático", "risk_score"),
        ("Aquecimento por ano", "warming_rate"),
        ("Variação de temperatura", "temperature_variability"),
        ("Dias de calor extremo", "heatwave_days"),
        ("Dias de frio extremo", "coldwave_days"),
        ("Diferença entre estações", "seasonal_amplitude"),
        ("Maior temperatura", "extreme_max"),
        ("Menor temperatura", "extreme_min"),
        ("Maior severidade de calor", "heatwave_severity"),
        ("Eventos fora do normal", "anomalies_detected"),
    ]
    return html.Div(
        [
            html.Div(
                [
                    html.Span(label, className="metric-label"),
                    html.Strong(summary.get(key, "n/a"), className="metric-value"),
                ],
                className="metric-cell",
            )
            for label, key in fields
        ],
        className="metric-grid",
    )


@callback(
    Output("city-profile-summary", "children"),
    Output("city-yearly-chart", "figure"),
    Output("city-anomaly-chart", "figure"),
    Output("city-anomaly-table", "children"),
    Input("city-profile-selector", "value"),
)
def update_city_profile(city):
    if not city:
        return _summary_grid({}), line_chart([], "year", "avg_temperature", "city", "Evolução da temperatura média anual"), scatter_timeline([], "date", "temperature_anomaly", "city", "z_score", "Dias muito acima ou abaixo do padrão histórico"), analytical_table([], "city-anomaly-empty")

    summary = safe_api_call(lambda: api_client.city_summary(city), {})
    yearly = safe_api_call(lambda: api_client.yearly_temperatures(city=city), [])
    anomalies = safe_api_call(lambda: api_client.anomalies(city=city, limit=200), [])

    return (
        _summary_grid(summary),
        line_chart(
            yearly,
            x="year",
            y="avg_temperature",
            color="city",
            title="Evolução da temperatura média anual",
        ),
        scatter_timeline(
            anomalies,
            x="date",
            y="temperature_anomaly",
            color="city",
            size="z_score",
            title="Dias muito acima ou abaixo do padrão histórico",
        ),
        analytical_table(
            anomalies,
            "city-anomaly-records-filtered",
            ["date", "temp_max", "temperature_anomaly", "z_score"],
            page_size=10,
        ),
    )
