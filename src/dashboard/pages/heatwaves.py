from __future__ import annotations

from dash import dcc, html

from dashboard.api.client import api_client
from dashboard.components.charts import histogram, horizontal_bar, scatter_timeline
from dashboard.components.tables import analytical_table
from dashboard.pages.common import page_header, safe_api_call, section


def layout() -> html.Div:
    heatwaves = safe_api_call(lambda: api_client.heatwaves(limit=100), [])
    severity = safe_api_call(lambda: api_client.heatwave_severity(limit=500), [])

    return html.Div(
        [
            page_header(
                "Ondas de Calor",
                "Dias de calor extremo e eventos prolongados que indicam maior pressão térmica sobre cada cidade.",
            ),
            html.Div(
                [
                    section(
                        "Dias de calor extremo",
                        dcc.Graph(
                            figure=horizontal_bar(
                                heatwaves,
                                x="heatwave_days",
                                y="city",
                                color="heatwave_days",
                                title="Número de dias acima do limite de calor",
                            ),
                        ),
                    ),
                    section(
                        "Eventos mais severos",
                        dcc.Graph(
                            figure=horizontal_bar(
                                severity,
                                x="severity_index",
                                y="city",
                                color="severity_index",
                                title="Severidade considerando duração e pico de temperatura",
                            ),
                        ),
                    ),
                ],
                className="grid two-col",
            ),
            html.Div(
                [
                    section(
                        "Duração dos eventos",
                        dcc.Graph(
                            figure=histogram(
                                severity,
                                x="duration_days",
                                color="city",
                                title="Quantos dias duraram as ondas de calor",
                            ),
                        ),
                    ),
                    section(
                        "Calendário dos eventos extremos",
                        dcc.Graph(
                            figure=scatter_timeline(
                                severity,
                                x="start_date",
                                y="max_temperature",
                                color="city",
                                size="severity_index",
                                title="Quando ocorreram e qual foi o pico de temperatura",
                            ),
                        ),
                    ),
                ],
                className="grid two-col",
            ),
            section(
                "Ondas de calor detectadas",
                analytical_table(
                    severity,
                    "heatwave-severity-table",
                    [
                        "city",
                        "sequence_id",
                        "start_date",
                        "end_date",
                        "duration_days",
                        "max_temperature",
                        "severity_index",
                    ],
                    page_size=12,
                ),
            ),
            section(
                "Total de dias de calor extremo",
                analytical_table(
                    heatwaves,
                    "heatwave-days-table",
                    ["city", "heatwave_days"],
                    page_size=8,
                ),
            ),
        ],
        className="page",
    )
