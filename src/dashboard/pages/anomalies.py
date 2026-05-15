from __future__ import annotations

from dash import Input, Output, callback, dcc, html

from dashboard.api.client import api_client
from dashboard.components.charts import histogram, scatter_timeline
from dashboard.components.filters import city_dropdown
from dashboard.components.tables import analytical_table
from dashboard.pages.common import page_header, safe_api_call, section


def layout() -> html.Div:
    cities = safe_api_call(api_client.cities, [])
    anomalies = safe_api_call(lambda: api_client.anomalies(limit=1000), [])

    return html.Div(
        [
            page_header(
                "Eventos de Temperatura Fora do Normal",
                "Dias em que a temperatura ficou muito acima ou muito abaixo do padrão histórico da cidade.",
            ),
            html.Div(
                [city_dropdown(cities, "anomaly-city-filter", multi=False)],
                className="filter-row",
            ),
            html.Div(
                [
                    section(
                        "Quando os desvios aconteceram",
                        dcc.Graph(
                            id="anomaly-timeline",
                            figure=scatter_timeline(
                                anomalies,
                                x="date",
                                y="temperature_anomaly",
                                color="city",
                                size="z_score",
                                title="Diferença em relação ao normal ao longo do tempo",
                            ),
                        ),
                    ),
                    section(
                        "Intensidade dos desvios",
                        dcc.Graph(
                            id="anomaly-distribution",
                            figure=histogram(
                                anomalies,
                                x="z_score",
                                color="city",
                                title="Quantos eventos foram leves ou muito extremos",
                            ),
                        ),
                    ),
                ],
                className="grid two-col",
            ),
            section(
                "Lista dos eventos encontrados",
                html.Div(
                    id="anomaly-table",
                    children=analytical_table(
                        anomalies,
                        "anomalies-table",
                        ["city", "date", "temp_max", "temperature_anomaly", "z_score"],
                        page_size=12,
                    ),
                ),
            ),
        ],
        className="page",
    )


@callback(
    Output("anomaly-timeline", "figure"),
    Output("anomaly-distribution", "figure"),
    Output("anomaly-table", "children"),
    Input("anomaly-city-filter", "value"),
)
def update_anomalies(city):
    anomalies = safe_api_call(
        lambda: api_client.anomalies(city=city, limit=1000),
        [],
    )
    return (
        scatter_timeline(
            anomalies,
            x="date",
            y="temperature_anomaly",
            color="city",
            size="z_score",
            title="Diferença em relação ao normal ao longo do tempo",
        ),
        histogram(
            anomalies,
            x="z_score",
            color="city",
            title="Quantos eventos foram leves ou muito extremos",
        ),
        analytical_table(
            anomalies,
            "anomalies-table-filtered",
            ["city", "date", "temp_max", "temperature_anomaly", "z_score"],
            page_size=12,
        ),
    )
