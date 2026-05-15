from __future__ import annotations

from dash import dcc, html


NAV_ITEMS = [
    ("Visão Geral", "/"),
    ("Aquecimento", "/warming-trends"),
    ("Eventos Anormais", "/anomalies"),
    ("Ondas de Calor", "/heatwaves"),
    ("Perfil da Cidade", "/city-analysis"),
]


def create_layout() -> html.Div:
    """Create the dashboard shell."""
    return html.Div(
        [
            dcc.Location(id="url"),
            html.Aside(
                [
                    html.Div(
                        [
                            html.Div("Monitor Climático", className="brand-title"),
                            html.Div("Painel de análise", className="brand-subtitle"),
                        ],
                        className="brand",
                    ),
                    html.Nav(
                        [
                            dcc.Link(label, href=href, className="nav-link")
                            for label, href in NAV_ITEMS
                        ],
                        className="nav",
                    ),
                    html.Div(
                        [
                            html.Div("Fonte dos dados", className="sidebar-label"),
                            html.Code("FastAPI :8000", className="sidebar-code"),
                        ],
                        className="sidebar-status",
                    ),
                ],
                className="sidebar",
            ),
            html.Main(id="page-content", className="content"),
        ],
        className="dashboard-shell",
    )
