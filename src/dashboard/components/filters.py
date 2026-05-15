from __future__ import annotations

from dash import dcc, html


def city_dropdown(cities: list[str], component_id: str, multi: bool = False):
    """Create a compact city selector."""
    return html.Div(
        [
            html.Label("Cidade", className="filter-label"),
            dcc.Dropdown(
                id=component_id,
                options=[{"label": city, "value": city} for city in cities],
                value=cities[:3] if multi else (cities[0] if cities else None),
                multi=multi,
                clearable=True,
                className="filter-control",
            ),
        ],
        className="filter-block",
    )
