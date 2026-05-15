from __future__ import annotations

from dash import dcc, html

from dashboard.api.client import api_client
from dashboard.components.charts import horizontal_bar
from dashboard.components.tables import analytical_table
from dashboard.pages.common import page_header, safe_api_call, section


def layout() -> html.Div:
    risk = safe_api_call(lambda: api_client.risk_ranking(limit=100), [])
    trends = safe_api_call(lambda: api_client.warming_trends(), [])
    severity = safe_api_call(lambda: api_client.heatwave_severity(limit=100), [])
    variability = safe_api_call(lambda: api_client.variability(limit=100), [])

    top_warming = sorted(
        trends,
        key=lambda row: row.get("warming_rate_per_year", 0),
        reverse=True,
    )
    top_severity = sorted(
        severity,
        key=lambda row: row.get("severity_index", 0),
        reverse=True,
    )

    return html.Div(
        [
            page_header(
                "Visão Geral do Clima",
                "Comparação entre cidades por risco climático, aquecimento, calor extremo e variação de temperatura.",
            ),
            html.Div(
                [
                    section(
                        "Cidades com maior risco climático",
                        analytical_table(
                            risk,
                            "overview-risk-table",
                            [
                                "city",
                                "risk_score",
                                "warming_rate",
                                "temperature_variability",
                                "heatwave_days",
                                "seasonal_amplitude",
                            ],
                            page_size=8,
                        ),
                    ),
                    section(
                        "Comparação do risco climático",
                        dcc.Graph(
                            figure=horizontal_bar(
                                risk,
                                x="risk_score",
                                y="city",
                                color="risk_score",
                                title="Quanto maior, maior a combinação de aquecimento, extremos e variação",
                            ),
                            config={"displayModeBar": False},
                        ),
                    ),
                ],
                className="grid two-col",
            ),
            html.Div(
                [
                    section(
                        "Cidades aquecendo mais rápido",
                        analytical_table(
                            top_warming,
                            "overview-warming-table",
                            ["city", "warming_rate_per_year"],
                            page_size=6,
                        ),
                    ),
                    section(
                        "Ondas de calor mais severas",
                        analytical_table(
                            top_severity,
                            "overview-severity-table",
                            [
                                "city",
                                "start_date",
                                "end_date",
                                "duration_days",
                                "max_temperature",
                                "severity_index",
                            ],
                            page_size=6,
                        ),
                    ),
                    section(
                        "Climas com maior variação",
                        analytical_table(
                            variability,
                            "overview-variability-table",
                            ["city", "temperature_variability"],
                            page_size=6,
                        ),
                    ),
                ],
                className="grid three-col",
            ),
        ],
        className="page",
    )
