from __future__ import annotations

from pathlib import Path

import pandas as pd

from utils.config import ClimateAnalyticsConfig, PipelineConfig
from utils.logger import get_logger

logger = get_logger(__name__)


def ensure_directories() -> None:
    """Create required output directories."""
    for directory in [
        PipelineConfig.OUTPUT_DATA_DIR,
        PipelineConfig.ANALYTICS_DIR,
        PipelineConfig.LOGS_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def export_dataframe(df: pd.DataFrame, filepath: Path) -> None:
    """Safely export a dataframe to CSV, creating parent directories first."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    logger.info("Exported CSV: %s", filepath)


def export_historical_data(df: pd.DataFrame) -> Path:
    """Export raw historical climate observations."""
    filepath = (
        PipelineConfig.OUTPUT_DATA_DIR
        / PipelineConfig.HISTORICAL_DATA_FILENAME
    )
    export_dataframe(df, filepath)
    return filepath


def export_analytics_results(results: dict[str, pd.DataFrame]) -> dict[str, Path]:
    """Export all analytics result dataframes to configured CSV files."""
    exported_files: dict[str, Path] = {}

    for result_name, filename in ClimateAnalyticsConfig.ANALYTICS_EXPORTS.items():
        if result_name not in results:
            logger.warning("Analytics result missing from export set: %s", result_name)
            continue

        filepath = PipelineConfig.ANALYTICS_DIR / filename
        export_dataframe(results[result_name], filepath)
        exported_files[result_name] = filepath

    return exported_files

