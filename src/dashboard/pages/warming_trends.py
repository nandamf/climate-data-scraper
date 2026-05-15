from __future__ import annotations

from dash import Input, Output, callback, dcc, html

from dashboard.api.client import api_client
from dashboard.components.charts import horizontal_bar, line_chart
from dashboard.components.filters import city_dropdown
from dashboard.components.tables import analytical_table
from dashboard.pages.common import page_header, safe_api_call, section


def layout() -> html.Div:
    cities = safe_api_call(api_client.cities, [])
    trends = safe_api_call(lambda: api_client.warming_trends(), [])
    yearly = safe_api_call(lambda: api_client.yearly_temperatures(), [])

    return html.Div(
        [
            page_header(
                "Tendência de Aquecimento",
                "Como a temperatura média anual mudou ao longo dos anos e quais cidades aquecem mais rápido.",
            ),
            html.Div(
                [
                    city_dropdown(cities, "warming-city-filter", multi=True),
                ],
                className="filter-row",
            ),
            html.Div(
                [
                    section(
                        "Temperatura média por ano",
                        dcc.Graph(
                            id="warming-yearly-chart",
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
                        "Velocidade de aquecimento",
                        dcc.Graph(
                            id="warming-rate-chart",
                            figure=horizontal_bar(
                                trends,
                                x="warming_rate_per_year",
                                y="city",
                                color="warming_rate_per_year",
                                title="Aumento médio estimado por ano",
                            ),
                        ),
                    ),
                ],
                className="grid two-col",
            ),
            section(
                "Tabela de aquecimento por cidade",
                html.Div(
                    id="warming-trend-table",
                    children=analytical_table(
                        trends,
                        "warming-trends-table",
                        ["city", "warming_rate_per_year"],
                    ),
                ),
            ),
        ],
        className="page",
    )


@callback(
    Output("warming-yearly-chart", "figure"),
    Output("warming-rate-chart", "figure"),
    Output("warming-trend-table", "children"),
    Input("warming-city-filter", "value"),
)
def update_warming(selected_cities):
    if isinstance(selected_cities, str):
        selected_cities = [selected_cities]

    yearly = safe_api_call(lambda: api_client.yearly_temperatures(), [])
    trends = safe_api_call(lambda: api_client.warming_trends(), [])

    if selected_cities:
        yearly = [row for row in yearly if row.get("city") in selected_cities]
        trends = [row for row in trends if row.get("city") in selected_cities]

    return (
        line_chart(
            yearly,
            x="year",
            y="avg_temperature",
            color="city",
            title="Evolução da temperatura média anual",
        ),
        horizontal_bar(
            trends,
            x="warming_rate_per_year",
            y="city",
            color="warming_rate_per_year",
            title="Aumento médio estimado por ano",
        ),
        analytical_table(
            trends,
            "warming-trends-table-filtered",
            ["city", "warming_rate_per_year"],
        ),
    )
