from __future__ import annotations

from typing import Any

from dash import dash_table, html

from dashboard.components.labels import label_for


def analytical_table(
    rows: list[dict[str, Any]],
    table_id: str,
    columns: list[str] | None = None,
    page_size: int = 10,
) -> html.Div:
    """Create a compact sortable/filterable analytical table."""
    if not rows:
        return html.Div("Nenhum registro encontrado para este critério.", className="empty-state")

    selected_columns = columns or list(rows[0].keys())
    return html.Div(
        dash_table.DataTable(
            id=table_id,
            data=[{column: row.get(column) for column in selected_columns} for row in rows],
            columns=[
                {"name": label_for(column), "id": column}
                for column in selected_columns
            ],
            page_size=page_size,
            sort_action="native",
            filter_action="native",
            style_as_list_view=True,
            style_cell={
                "fontFamily": "Inter, Segoe UI, Arial, sans-serif",
                "fontSize": "12px",
                "padding": "7px 8px",
                "border": "1px solid #d9dee7",
                "textAlign": "left",
                "whiteSpace": "normal",
                "height": "auto",
            },
            style_header={
                "backgroundColor": "#eef2f6",
                "fontWeight": "600",
                "color": "#1e2933",
                "border": "1px solid #cbd5df",
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "#f8fafc"},
            ],
        ),
        className="table-shell",
    )
