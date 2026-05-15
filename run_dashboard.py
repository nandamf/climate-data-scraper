"""Dash dashboard entrypoint.

Run with:
    python run_dashboard.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dashboard.app import app


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8050,
        debug=False,
    )
