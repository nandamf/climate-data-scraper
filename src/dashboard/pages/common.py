from __future__ import annotations

from typing import Any, Callable

from dash import html
from requests import RequestException


def safe_api_call(call: Callable[[], Any], fallback: Any) -> Any:
    """Return API data or a fallback when the backend is not reachable."""
    try:
        return call()
    except RequestException:
        return fallback


def page_header(title: str, subtitle: str) -> html.Div:
    return html.Div(
        [
            html.H1(title),
            html.P(subtitle),
        ],
        className="page-header",
    )


def section(title: str, children) -> html.Section:
    return html.Section(
        [
            html.Div(title, className="section-title"),
            children,
        ],
        className="panel",
    )


def graph_panel(title: str, graph) -> html.Section:
    return section(title, graph)

