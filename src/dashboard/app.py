from __future__ import annotations

from pathlib import Path

from dash import Dash, Input, Output

from dashboard.layout import create_layout
from dashboard.pages import anomalies, city_analysis, heatwaves, overview, warming_trends

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def create_app() -> Dash:
    """Create and configure the Dash dashboard."""
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        title="Climate Intelligence Observatory",
        assets_folder=str(ASSETS_DIR),
    )
    app.layout = create_layout()

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def route_page(pathname: str):
        if pathname == "/warming-trends":
            return warming_trends.layout()
        if pathname == "/anomalies":
            return anomalies.layout()
        if pathname == "/heatwaves":
            return heatwaves.layout()
        if pathname == "/city-analysis":
            return city_analysis.layout()
        return overview.layout()

    return app


app = create_app()
