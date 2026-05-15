from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.components.labels import labels_for


PLOT_TEMPLATE = "plotly_white"
CHART_HEIGHT = 340


def empty_figure(message: str = "Sem dados para este critério") -> go.Figure:
    """Return a neutral empty chart with a technical status message."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 13, "color": "#627386"},
    )
    fig.update_layout(
        template=PLOT_TEMPLATE,
        height=CHART_HEIGHT,
        margin={"l": 30, "r": 20, "t": 35, "b": 30},
        xaxis={"visible": False},
        yaxis={"visible": False},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
    )
    return fig


def _df(rows: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(rows or [])


def horizontal_bar(
    rows: list[dict[str, Any]],
    x: str,
    y: str,
    title: str,
    color: str | None = None,
) -> go.Figure:
    df = _df(rows)
    if df.empty or x not in df or y not in df:
        return empty_figure()

    df = df.sort_values(x, ascending=True)
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        color=color,
        title=title,
        template=PLOT_TEMPLATE,
        color_continuous_scale="Blues",
        labels=labels_for([x, y, color] if color else [x, y]),
    )
    fig.update_layout(
        height=CHART_HEIGHT,
        margin={"l": 75, "r": 20, "t": 45, "b": 35},
        coloraxis_showscale=False,
        legend_title_text="Cidade",
        title={"font": {"size": 14}},
    )
    return fig


def line_chart(
    rows: list[dict[str, Any]],
    x: str,
    y: str,
    color: str,
    title: str,
) -> go.Figure:
    df = _df(rows)
    if df.empty or x not in df or y not in df:
        return empty_figure("Sem série anual para exibir")

    df[x] = pd.to_numeric(df[x], errors="coerce")
    df[y] = pd.to_numeric(df[y], errors="coerce")
    df = df.dropna(subset=[x, y])
    if df.empty:
        return empty_figure()

    fig = px.line(
        df.sort_values(x),
        x=x,
        y=y,
        color=color,
        markers=True,
        title=title,
        template=PLOT_TEMPLATE,
        labels=labels_for([x, y, color]),
    )
    fig.update_layout(
        height=390,
        margin={"l": 55, "r": 20, "t": 45, "b": 45},
        legend_title_text="Cidade",
        title={"font": {"size": 14}},
        xaxis_title=labels_for([x])[x],
        yaxis_title=labels_for([y])[y],
    )
    return fig


def scatter_timeline(
    rows: list[dict[str, Any]],
    x: str,
    y: str,
    color: str,
    size: str | None,
    title: str,
) -> go.Figure:
    df = _df(rows)
    if df.empty or x not in df or y not in df:
        return empty_figure()

    size_column = size if size and size in df else None
    if size_column:
        visual_size_column = f"{size_column}_marker_size"
        df[visual_size_column] = pd.to_numeric(
            df[size_column],
            errors="coerce",
        ).abs()
    else:
        visual_size_column = None

    hover_columns = [
        column for column in df.columns if not column.endswith("_marker_size")
    ]

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color if color in df else None,
        size=visual_size_column,
        hover_data=hover_columns,
        title=title,
        template=PLOT_TEMPLATE,
        labels=labels_for([x, y, color, size_column] if size_column else [x, y, color]),
    )
    fig.update_layout(
        height=390,
        margin={"l": 55, "r": 20, "t": 45, "b": 45},
        title={"font": {"size": 14}},
        legend_title_text="Cidade",
    )
    return fig


def histogram(
    rows: list[dict[str, Any]],
    x: str,
    color: str | None,
    title: str,
) -> go.Figure:
    df = _df(rows)
    if df.empty or x not in df:
        return empty_figure()

    fig = px.histogram(
        df,
        x=x,
        color=color if color and color in df else None,
        nbins=30,
        title=title,
        template=PLOT_TEMPLATE,
        labels=labels_for([x, color] if color else [x]),
    )
    fig.update_xaxes(title_text=labels_for([x])[x])
    fig.update_yaxes(title_text="Número de registros")
    fig.update_layout(
        height=CHART_HEIGHT,
        margin={"l": 55, "r": 20, "t": 45, "b": 45},
        bargap=0.08,
        legend_title_text="Cidade",
        title={"font": {"size": 14}},
    )
    return fig
